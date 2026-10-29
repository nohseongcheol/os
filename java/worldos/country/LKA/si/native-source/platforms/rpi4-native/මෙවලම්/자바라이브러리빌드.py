"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 කියවීම 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(기준경로, ක්_රියාත්මක_කරන්න_විධානය):
    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = 기준경로 / 'build/java-library'
    පන්තිය_පෙත = 출력결과 / 'classes'
    පන්තිය_පෙත.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((기준경로 / '한국어자바').rglob('*.java'))
    ක්_රියාත්මක_කරන්න_විධානය(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', පන්තිය_පෙත] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(기준경로 / '한국어자바').with_suffix('.class')
        ගෙවීම්_භාරය_දත්ත = (පන්තිය_පෙත / 상대경로).read_bytes()
        නම = str(상대경로).replace('/', '.')
        if len(ගෙවීම්_භාරය_දත්ත) > 16384 or len(නම.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + නම)
        항목들.append((상대경로, නම, ගෙවීම්_භාරය_දත්ත))
    ශීර්ෂය_අගය = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *නම; const unsigned char *දත්ත; unsigned ප්_රමාණය; } 자바자원;']
    for 순번, (_, නම, ගෙවීම්_භාරය_දත්ත) in enumerate(항목들):
        ශීර්ෂය_අගය.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in ගෙවීම්_භාරය_දත්ත)))
    ශීර්ෂය_අගය.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, නම, ගෙවීම්_භාරය_දත්ත) in enumerate(항목들):
        ශීර්ෂය_අගය.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(නම, ensure_ascii=False), 순번, len(ගෙවීම්_භාරය_දත්ත)))
    ශීර්ෂය_අගය.append('};')
    (기준경로 / 'build/user/java-resources.h').write_text('\n'.join(ශීර්ෂය_අගය) + '\n', encoding='utf-8')
    배포경로 = 기준경로 / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, ගෙවීම්_භාරය_දත්ත in 항목들:
            පද්ධති_තොරතුරු = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); පද්ධති_තොරතුරු.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(පද්ධති_තොරතුරු, ගෙවීම්_භාරය_දත්ත)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as සංරක්ෂිතය:
        for 원본주소 in 원문목록:
            පද්ධති_තොරතුරු = zipfile.ZipInfo(str(원본주소.relative_to(기준경로 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); පද්ධති_තොරතුරු.compress_type = zipfile.ZIP_DEFLATED
            සංරක්ෂිතය.writestr(පද්ධති_තොරතුරු, 원본주소.read_bytes())
