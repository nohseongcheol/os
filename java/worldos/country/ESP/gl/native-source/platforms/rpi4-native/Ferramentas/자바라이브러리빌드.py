"""자체 JVM용 Galego class/JAR와 EL0에 넣을 Lectura 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(raíz_camiño, executar_comando):
    (raíz_camiño / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = raíz_camiño / 'build/java-library'
    Clase_camiño = 출력결과 / 'classes'
    Clase_camiño.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((raíz_camiño / '한국어자바').rglob('*.java'))
    executar_comando(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Clase_camiño] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(raíz_camiño / '한국어자바').with_suffix('.class')
        carga_datos_60367a51 = (Clase_camiño / 상대경로).read_bytes()
        Nome = str(상대경로).replace('/', '.')
        if len(carga_datos_60367a51) > 16384 or len(Nome.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Nome)
        항목들.append((상대경로, Nome, carga_datos_60367a51))
    Cabeceira_VALOR = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Nome; const unsigned char *datos; unsigned Tamaño; } 자바자원;']
    for 순번, (_, Nome, carga_datos_60367a51) in enumerate(항목들):
        Cabeceira_VALOR.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SEGUNDO_VALOR) for SEGUNDO_VALOR in carga_datos_60367a51)))
    Cabeceira_VALOR.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Nome, carga_datos_60367a51) in enumerate(항목들):
        Cabeceira_VALOR.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Nome, ensure_ascii=False), 순번, len(carga_datos_60367a51)))
    Cabeceira_VALOR.append('};')
    (raíz_camiño / 'build/user/java-resources.h').write_text('\n'.join(Cabeceira_VALOR) + '\n', encoding='utf-8')
    배포경로 = raíz_camiño / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, carga_datos_60367a51 in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, carga_datos_60367a51)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arquivo:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(raíz_camiño / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arquivo.writestr(msinfo32_exe, 원본주소.read_bytes())
