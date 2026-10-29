"""자체 JVM용 Gaeilge class/JAR와 EL0에 넣을 Léigh 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(fréamh_cosán, Rith_ordú):
    (fréamh_cosán / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = fréamh_cosán / 'build/java-library'
    aicme_cosán = 출력결과 / 'classes'
    aicme_cosán.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((fréamh_cosán / '한국어자바').rglob('*.java'))
    Rith_ordú(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', aicme_cosán] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(fréamh_cosán / '한국어자바').with_suffix('.class')
        pálasta_sonraí = (aicme_cosán / 상대경로).read_bytes()
        Ainm = str(상대경로).replace('/', '.')
        if len(pálasta_sonraí) > 16384 or len(Ainm.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Ainm)
        항목들.append((상대경로, Ainm, pálasta_sonraí))
    Ceanntásc_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Ainm; const unsigned char *sonraí; unsigned Méid; } 자바자원;']
    for 순번, (_, Ainm, pálasta_sonraí) in enumerate(항목들):
        Ceanntásc_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in pálasta_sonraí)))
    Ceanntásc_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Ainm, pálasta_sonraí) in enumerate(항목들):
        Ceanntásc_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Ainm, ensure_ascii=False), 순번, len(pálasta_sonraí)))
    Ceanntásc_VALUE.append('};')
    (fréamh_cosán / 'build/user/java-resources.h').write_text('\n'.join(Ceanntásc_VALUE) + '\n', encoding='utf-8')
    배포경로 = fréamh_cosán / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, pálasta_sonraí in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, pálasta_sonraí)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Cartlann:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(fréamh_cosán / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Cartlann.writestr(msinfo32_exe, 원본주소.read_bytes())
