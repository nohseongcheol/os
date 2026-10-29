"""নিজ JVM용 বাংলা class/JAR와 EL0에 넣을 পড়া 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(মূল_পথ, কার্যকর_করুন_আদেশ):
    (মূল_পথ / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = মূল_পথ / 'build/java-library'
    শ্রেণী_পথ = 출력결과 / 'classes'
    শ্রেণী_পথ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((মূল_পথ / '한국어자바').rglob('*.java'))
    কার্যকর_করুন_আদেশ(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', শ্রেণী_পথ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(মূল_পথ / '한국어자바').with_suffix('.class')
        পেলোড_ডাটা = (শ্রেণী_পথ / 상대경로).read_bytes()
        নাম = str(상대경로).replace('/', '.')
        if len(পেলোড_ডাটা) > 16384 or len(নাম.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + নাম)
        항목들.append((상대경로, নাম, পেলোড_ডাটা))
    হেডার_মান = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *নাম; const unsigned char *ডাটা; unsigned আকার; } 자바자원;']
    for 순번, (_, নাম, পেলোড_ডাটা) in enumerate(항목들):
        হেডার_মান.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in পেলোড_ডাটা)))
    হেডার_মান.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, নাম, পেলোড_ডাটা) in enumerate(항목들):
        হেডার_মান.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(নাম, ensure_ascii=False), 순번, len(পেলোড_ডাটা)))
    হেডার_মান.append('};')
    (মূল_পথ / 'build/user/java-resources.h').write_text('\n'.join(হেডার_মান) + '\n', encoding='utf-8')
    배포경로 = মূল_পথ / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, পেলোড_ডাটা in 항목들:
            সিসটেম_তথ্য = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); সিসটেম_তথ্য.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(সিসটেম_তথ্য, পেলোড_ডাটা)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as সংগ্রহ_করা:
        for 원본주소 in 원문목록:
            সিসটেম_তথ্য = zipfile.ZipInfo(str(원본주소.relative_to(মূল_পথ / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); সিসটেম_তথ্য.compress_type = zipfile.ZIP_DEFLATED
            সংগ্রহ_করা.writestr(সিসটেম_তথ্য, 원본주소.read_bytes())
