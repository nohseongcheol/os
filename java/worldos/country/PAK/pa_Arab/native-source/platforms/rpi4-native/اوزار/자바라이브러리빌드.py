"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 읽기 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(기준경로, نفاذ_کرو_حکم):
    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = 기준경로 / 'build/java-library'
    درجہ_راہ = 출력결과 / 'classes'
    درجہ_راہ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((기준경로 / '한국어자바').rglob('*.java'))
    نفاذ_کرو_حکم(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', درجہ_راہ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(기준경로 / '한국어자바').with_suffix('.class')
        پے_لوڈ_کوائف = (درجہ_راہ / 상대경로).read_bytes()
        ناں = str(상대경로).replace('/', '.')
        if len(پے_لوڈ_کوائف) > 16384 or len(ناں.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + ناں)
        항목들.append((상대경로, ناں, پے_لوڈ_کوائف))
    سرتحریر_قدر = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *ناں; const unsigned char *کوائف; unsigned سائز; } 자바자원;']
    for 순번, (_, ناں, پے_لوڈ_کوائف) in enumerate(항목들):
        سرتحریر_قدر.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in پے_لوڈ_کوائف)))
    سرتحریر_قدر.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, ناں, پے_لوڈ_کوائف) in enumerate(항목들):
        سرتحریر_قدر.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(ناں, ensure_ascii=False), 순번, len(پے_لوڈ_کوائف)))
    سرتحریر_قدر.append('};')
    (기준경로 / 'build/user/java-resources.h').write_text('\n'.join(سرتحریر_قدر) + '\n', encoding='utf-8')
    배포경로 = 기준경로 / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, پے_لوڈ_کوائف in 항목들:
            سسٹم_دی_معلومات = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); سسٹم_دی_معلومات.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(سسٹم_دی_معلومات, پے_لوڈ_کوائف)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as محفوظہ:
        for 원본주소 in 원문목록:
            سسٹم_دی_معلومات = zipfile.ZipInfo(str(원본주소.relative_to(기준경로 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); سسٹم_دی_معلومات.compress_type = zipfile.ZIP_DEFLATED
            محفوظہ.writestr(سسٹم_دی_معلومات, 원본주소.read_bytes())
