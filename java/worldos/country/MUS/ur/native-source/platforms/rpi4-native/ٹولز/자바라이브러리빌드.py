"""اپنا JVM용 اردو class/JAR와 EL0에 넣을 پڑھیں 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(روٹ_راہ, نفاذ_کریں_حکم):
    (روٹ_راہ / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = روٹ_راہ / 'build/java-library'
    صنف_راہ = 출력결과 / 'classes'
    صنف_راہ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((روٹ_راہ / '한국어자바').rglob('*.java'))
    نفاذ_کریں_حکم(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', صنف_راہ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(روٹ_راہ / '한국어자바').with_suffix('.class')
        پے_لوڈ_کوائف = (صنف_راہ / 상대경로).read_bytes()
        نام = str(상대경로).replace('/', '.')
        if len(پے_لوڈ_کوائف) > 16384 or len(نام.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + نام)
        항목들.append((상대경로, نام, پے_لوڈ_کوائف))
    سرصفحہ_قدر = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *نام; const unsigned char *کوائف; unsigned حجم; } 자바자원;']
    for 순번, (_, نام, پے_لوڈ_کوائف) in enumerate(항목들):
        سرصفحہ_قدر.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in پے_لوڈ_کوائف)))
    سرصفحہ_قدر.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, نام, پے_لوڈ_کوائف) in enumerate(항목들):
        سرصفحہ_قدر.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(نام, ensure_ascii=False), 순번, len(پے_لوڈ_کوائف)))
    سرصفحہ_قدر.append('};')
    (روٹ_راہ / 'build/user/java-resources.h').write_text('\n'.join(سرصفحہ_قدر) + '\n', encoding='utf-8')
    배포경로 = روٹ_راہ / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, پے_لوڈ_کوائف in 항목들:
            نظام_کی_معلومات = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); نظام_کی_معلومات.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(نظام_کی_معلومات, پے_لوڈ_کوائف)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as محفوظ:
        for 원본주소 in 원문목록:
            نظام_کی_معلومات = zipfile.ZipInfo(str(원본주소.relative_to(روٹ_راہ / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); نظام_کی_معلومات.compress_type = zipfile.ZIP_DEFLATED
            محفوظ.writestr(نظام_کی_معلومات, 원본주소.read_bytes())
