"""자체 JVM용 ગુજરાતી class/JAR와 EL0에 넣을 વાંચો 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(રૂટ_પાથ, અમલ_કરો_આદેશ):
    (રૂટ_પાથ / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = રૂટ_પાથ / 'build/java-library'
    વર્ગ_પાથ = 출력결과 / 'classes'
    વર્ગ_પાથ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((રૂટ_પાથ / '한국어자바').rglob('*.java'))
    અમલ_કરો_આદેશ(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', વર્ગ_પાથ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(રૂટ_પાથ / '한국어자바').with_suffix('.class')
        પેલોડ_ડેટા = (વર્ગ_પાથ / 상대경로).read_bytes()
        નામ = str(상대경로).replace('/', '.')
        if len(પેલોડ_ડેટા) > 16384 or len(નામ.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + નામ)
        항목들.append((상대경로, નામ, પેલોડ_ડેટા))
    શીર્ષલેખ_મૂલ્ય = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *નામ; const unsigned char *ડેટા; unsigned માપ; } 자바자원;']
    for 순번, (_, નામ, પેલોડ_ડેટા) in enumerate(항목들):
        શીર્ષલેખ_મૂલ્ય.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in પેલોડ_ડેટા)))
    શીર્ષલેખ_મૂલ્ય.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, નામ, પેલોડ_ડેટા) in enumerate(항목들):
        શીર્ષલેખ_મૂલ્ય.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(નામ, ensure_ascii=False), 순번, len(પેલોડ_ડેટા)))
    શીર્ષલેખ_મૂલ્ય.append('};')
    (રૂટ_પાથ / 'build/user/java-resources.h').write_text('\n'.join(શીર્ષલેખ_મૂલ્ય) + '\n', encoding='utf-8')
    배포경로 = રૂટ_પાથ / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, પેલોડ_ડેટા in 항목들:
            સિસ્ટમ_માહિતી = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); સિસ્ટમ_માહિતી.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(સિસ્ટમ_માહિતી, પેલોડ_ડેટા)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as સંગ્રહ:
        for 원본주소 in 원문목록:
            સિસ્ટમ_માહિતી = zipfile.ZipInfo(str(원본주소.relative_to(રૂટ_પાથ / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); સિસ્ટમ_માહિતી.compress_type = zipfile.ZIP_DEFLATED
            સંગ્રહ.writestr(સિસ્ટમ_માહિતી, 원본주소.read_bytes())
