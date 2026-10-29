"""nativo JVM용 Português class/JAR와 EL0에 넣을 Leitura 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(raiz_caminho, Executar_comando):
    (raiz_caminho / 'build/user').mkdir(parents=True, exist_ok=True)
    saída = raiz_caminho / 'build/java-library'
    aula_caminho = saída / 'classes'
    aula_caminho.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((raiz_caminho / '한국어자바').rglob('*.java'))
    Executar_comando(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', aula_caminho] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        caminho_relativo = 원본주소.relative_to(raiz_caminho / '한국어자바').with_suffix('.class')
        carga_dados = (aula_caminho / caminho_relativo).read_bytes()
        Nome = str(caminho_relativo).replace('/', '.')
        if len(carga_dados) > 16384 or len(Nome.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Nome)
        항목들.append((caminho_relativo, Nome, carga_dados))
    Cabeçalho_VALOR = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Nome; const unsigned char *dados; unsigned Tamanho; } 자바자원;']
    for 순번, (_, Nome, carga_dados) in enumerate(항목들):
        Cabeçalho_VALOR.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SEGUNDO_VALOR) for SEGUNDO_VALOR in carga_dados)))
    Cabeçalho_VALOR.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Nome, carga_dados) in enumerate(항목들):
        Cabeçalho_VALOR.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Nome, ensure_ascii=False), 순번, len(carga_dados)))
    Cabeçalho_VALOR.append('};')
    (raiz_caminho / 'build/user/java-resources.h').write_text('\n'.join(Cabeçalho_VALOR) + '\n', encoding='utf-8')
    distribuição_caminho = raiz_caminho / 'dist'; distribuição_caminho.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(distribuição_caminho / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for caminho_relativo, _, carga_dados in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(caminho_relativo), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, carga_dados)
    with zipfile.ZipFile(str(distribuição_caminho / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as arquivo:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(raiz_caminho / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            arquivo.writestr(msinfo32_exe, 원본주소.read_bytes())
