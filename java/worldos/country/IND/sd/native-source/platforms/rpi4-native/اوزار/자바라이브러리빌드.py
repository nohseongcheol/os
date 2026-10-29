"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 읽기 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(기준경로, تعميل_ڪرڻ_حڪم):
    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = 기준경로 / 'build/java-library'
    درجو_راههه = 출력결과 / 'classes'
    درجو_راههه.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((기준경로 / '한국어자바').rglob('*.java'))
    تعميل_ڪرڻ_حڪم(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', درجو_راههه] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(기준경로 / '한국어자바').with_suffix('.class')
        بنيادي_بار_ڪوائف = (درجو_راههه / 상대경로).read_bytes()
        نالو = str(상대경로).replace('/', '.')
        if len(بنيادي_بار_ڪوائف) > 16384 or len(نالو.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + نالو)
        항목들.append((상대경로, نالو, بنيادي_بار_ڪوائف))
    هيڊر_قدر = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *نالو; const unsigned char *ڪوائف; unsigned سائيز; } 자바자원;']
    for 순번, (_, نالو, بنيادي_بار_ڪوائف) in enumerate(항목들):
        هيڊر_قدر.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in بنيادي_بار_ڪوائف)))
    هيڊر_قدر.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, نالو, بنيادي_بار_ڪوائف) in enumerate(항목들):
        هيڊر_قدر.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(نالو, ensure_ascii=False), 순번, len(بنيادي_بار_ڪوائف)))
    هيڊر_قدر.append('};')
    (기준경로 / 'build/user/java-resources.h').write_text('\n'.join(هيڊر_قدر) + '\n', encoding='utf-8')
    배포경로 = 기준경로 / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, بنيادي_بار_ڪوائف in 항목들:
            سسٽم_معلومات = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); سسٽم_معلومات.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(سسٽم_معلومات, بنيادي_بار_ڪوائف)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as محفوظ:
        for 원본주소 in 원문목록:
            سسٽم_معلومات = zipfile.ZipInfo(str(원본주소.relative_to(기준경로 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); سسٽم_معلومات.compress_type = zipfile.ZIP_DEFLATED
            محفوظ.writestr(سسٽم_معلومات, 원본주소.read_bytes())
