"""ذاتي JVM용 العربية class/JAR와 EL0에 넣을 قراءة 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(جذر_مسار, ينفذ_أمر):
    (جذر_مسار / 'build/user').mkdir(parents=True, exist_ok=True)
    الناتج = جذر_مسار / 'build/java-library'
    فئة_مسار = الناتج / 'classes'
    فئة_مسار.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((جذر_مسار / '한국어자바').rglob('*.java'))
    ينفذ_أمر(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', فئة_مسار] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        مسار_نسبي = 원본주소.relative_to(جذر_مسار / '한국어자바').with_suffix('.class')
        حمولة_بيانات = (فئة_مسار / مسار_نسبي).read_bytes()
        اسم = str(مسار_نسبي).replace('/', '.')
        if len(حمولة_بيانات) > 16384 or len(اسم.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + اسم)
        항목들.append((مسار_نسبي, اسم, حمولة_بيانات))
    عنوان_قيمة_4a42eba5 = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *اسم; const unsigned char *بيانات; unsigned حجم; } 자바자원;']
    for 순번, (_, اسم, حمولة_بيانات) in enumerate(항목들):
        عنوان_قيمة_4a42eba5.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in حمولة_بيانات)))
    عنوان_قيمة_4a42eba5.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, اسم, حمولة_بيانات) in enumerate(항목들):
        عنوان_قيمة_4a42eba5.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(اسم, ensure_ascii=False), 순번, len(حمولة_بيانات)))
    عنوان_قيمة_4a42eba5.append('};')
    (جذر_مسار / 'build/user/java-resources.h').write_text('\n'.join(عنوان_قيمة_4a42eba5) + '\n', encoding='utf-8')
    توزيع_مسار = جذر_مسار / 'dist'; توزيع_مسار.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(توزيع_مسار / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for مسار_نسبي, _, حمولة_بيانات in 항목들:
            معلومات_النظام = zipfile.ZipInfo(str(مسار_نسبي), date_time=(1980, 1, 1, 0, 0, 0)); معلومات_النظام.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(معلومات_النظام, حمولة_بيانات)
    with zipfile.ZipFile(str(توزيع_مسار / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as أرشيف:
        for 원본주소 in 원문목록:
            معلومات_النظام = zipfile.ZipInfo(str(원본주소.relative_to(جذر_مسار / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); معلومات_النظام.compress_type = zipfile.ZIP_DEFLATED
            أرشيف.writestr(معلومات_النظام, 원본주소.read_bytes())
