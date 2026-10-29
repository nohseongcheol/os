"""propi JVM용 Català class/JAR와 EL0에 넣을 Lectura 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(rel_camí, Executa_ordre):
    (rel_camí / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = rel_camí / 'build/java-library'
    Classe_camí = 출력결과 / 'classes'
    Classe_camí.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((rel_camí / '한국어자바').rglob('*.java'))
    Executa_ordre(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Classe_camí] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(rel_camí / '한국어자바').with_suffix('.class')
        càrrega_dades = (Classe_camí / 상대경로).read_bytes()
        Nom = str(상대경로).replace('/', '.')
        if len(càrrega_dades) > 16384 or len(Nom.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Nom)
        항목들.append((상대경로, Nom, càrrega_dades))
    Capçalera_VALOR = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Nom; const unsigned char *dades; unsigned Mida; } 자바자원;']
    for 순번, (_, Nom, càrrega_dades) in enumerate(항목들):
        Capçalera_VALOR.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SEGON_VALOR) for SEGON_VALOR in càrrega_dades)))
    Capçalera_VALOR.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Nom, càrrega_dades) in enumerate(항목들):
        Capçalera_VALOR.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Nom, ensure_ascii=False), 순번, len(càrrega_dades)))
    Capçalera_VALOR.append('};')
    (rel_camí / 'build/user/java-resources.h').write_text('\n'.join(Capçalera_VALOR) + '\n', encoding='utf-8')
    배포경로 = rel_camí / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, càrrega_dades in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, càrrega_dades)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arxiu:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(rel_camí / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arxiu.writestr(msinfo32_exe, 원본주소.read_bytes())
