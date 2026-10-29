"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 পড়া 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(ৰুট_পথ, নিষ্পাদন_আদেশ):
    (ৰুট_পথ / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = ৰুট_পথ / 'build/java-library'
    শ্ৰেণী_পথ = 출력결과 / 'classes'
    শ্ৰেণী_পথ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((ৰুট_পথ / '한국어자바').rglob('*.java'))
    নিষ্পাদন_আদেশ(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', শ্ৰেণী_পথ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(ৰুট_পথ / '한국어자바').with_suffix('.class')
        প্লেল_ড_ডাটা = (শ্ৰেণী_পথ / 상대경로).read_bytes()
        নাম = str(상대경로).replace('/', '.')
        if len(প্লেল_ড_ডাটা) > 16384 or len(নাম.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + নাম)
        항목들.append((상대경로, নাম, প্লেল_ড_ডাটা))
    শিৰো_মান = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *নাম; const unsigned char *ডাটা; unsigned মাপ; } 자바자원;']
    for 순번, (_, নাম, প্লেল_ড_ডাটা) in enumerate(항목들):
        শিৰো_মান.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in প্লেল_ড_ডাটা)))
    শিৰো_মান.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, নাম, প্লেল_ড_ডাটা) in enumerate(항목들):
        শিৰো_মান.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(নাম, ensure_ascii=False), 순번, len(প্লেল_ড_ডাটা)))
    শিৰো_মান.append('};')
    (ৰুট_পথ / 'build/user/java-resources.h').write_text('\n'.join(শিৰো_মান) + '\n', encoding='utf-8')
    배포경로 = ৰুট_পথ / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, প্লেল_ড_ডাটা in 항목들:
            ছিষ্টেম_তথ্য = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); ছিষ্টেম_তথ্য.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(ছিষ্টেম_তথ্য, প্লেল_ড_ডাটা)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as অভিলেখাগাৰ:
        for 원본주소 in 원문목록:
            ছিষ্টেম_তথ্য = zipfile.ZipInfo(str(원본주소.relative_to(ৰুট_পথ / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); ছিষ্টেম_তথ্য.compress_type = zipfile.ZIP_DEFLATED
            অভিলেখাগাৰ.writestr(ছিষ্টেম_তথ্য, 원본주소.read_bytes())
