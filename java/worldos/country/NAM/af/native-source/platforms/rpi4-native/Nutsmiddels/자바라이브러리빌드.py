"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 Lees 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(wortel_pad, uitvoer_bevel):
    (wortel_pad / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = wortel_pad / 'build/java-library'
    Klas_pad = 출력결과 / 'classes'
    Klas_pad.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((wortel_pad / '한국어자바').rglob('*.java'))
    uitvoer_bevel(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Klas_pad] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(wortel_pad / '한국어자바').with_suffix('.class')
        lading_data = (Klas_pad / 상대경로).read_bytes()
        Naam = str(상대경로).replace('/', '.')
        if len(lading_data) > 16384 or len(Naam.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Naam)
        항목들.append((상대경로, Naam, lading_data))
    Loopkop_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Naam; const unsigned char *data; unsigned Grootte; } 자바자원;']
    for 순번, (_, Naam, lading_data) in enumerate(항목들):
        Loopkop_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in lading_data)))
    Loopkop_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Naam, lading_data) in enumerate(항목들):
        Loopkop_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Naam, ensure_ascii=False), 순번, len(lading_data)))
    Loopkop_VALUE.append('};')
    (wortel_pad / 'build/user/java-resources.h').write_text('\n'.join(Loopkop_VALUE) + '\n', encoding='utf-8')
    배포경로 = wortel_pad / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, lading_data in 항목들:
            Stelselinfo = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); Stelselinfo.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(Stelselinfo, lading_data)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Argief:
        for 원본주소 in 원문목록:
            Stelselinfo = zipfile.ZipInfo(str(원본주소.relative_to(wortel_pad / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); Stelselinfo.compress_type = zipfile.ZIP_DEFLATED
            Argief.writestr(Stelselinfo, 원본주소.read_bytes())
