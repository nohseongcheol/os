"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 읽기 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(기준경로, diragatsa_Taelo):
    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = 기준경로 / 'build/java-library'
    mofuta_tsela = 출력결과 / 'classes'
    mofuta_tsela.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((기준경로 / '한국어자바').rglob('*.java'))
    diragatsa_Taelo(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', mofuta_tsela] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(기준경로 / '한국어자바').with_suffix('.class')
        selekanyo_sa_tshedimosetso_tshedimosetso = (mofuta_tsela / 상대경로).read_bytes()
        leina = str(상대경로).replace('/', '.')
        if len(selekanyo_sa_tshedimosetso_tshedimosetso) > 16384 or len(leina.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + leina)
        항목들.append((상대경로, leina, selekanyo_sa_tshedimosetso_tshedimosetso))
    setlhogo_Boleng = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *leina; const unsigned char *tshedimosetso; unsigned lekanya; } 자바자원;']
    for 순번, (_, leina, selekanyo_sa_tshedimosetso_tshedimosetso) in enumerate(항목들):
        setlhogo_Boleng.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in selekanyo_sa_tshedimosetso_tshedimosetso)))
    setlhogo_Boleng.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, leina, selekanyo_sa_tshedimosetso_tshedimosetso) in enumerate(항목들):
        setlhogo_Boleng.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(leina, ensure_ascii=False), 순번, len(selekanyo_sa_tshedimosetso_tshedimosetso)))
    setlhogo_Boleng.append('};')
    (기준경로 / 'build/user/java-resources.h').write_text('\n'.join(setlhogo_Boleng) + '\n', encoding='utf-8')
    배포경로 = 기준경로 / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, selekanyo_sa_tshedimosetso_tshedimosetso in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, selekanyo_sa_tshedimosetso_tshedimosetso)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as boloka:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(기준경로 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            boloka.writestr(msinfo32_exe, 원본주소.read_bytes())
