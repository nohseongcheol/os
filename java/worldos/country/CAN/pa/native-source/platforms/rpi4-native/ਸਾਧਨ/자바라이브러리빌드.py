"""자체 JVM용 ਪੰਜਾਬੀ class/JAR와 EL0에 넣을 ਪੜ੍ਹਨ 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(ਰੂਟ_ਰਸਤਾ, ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼):
    (ਰੂਟ_ਰਸਤਾ / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = ਰੂਟ_ਰਸਤਾ / 'build/java-library'
    ਸ੍ਰੇਣੀ_ਰਸਤਾ = 출력결과 / 'classes'
    ਸ੍ਰੇਣੀ_ਰਸਤਾ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((ਰੂਟ_ਰਸਤਾ / '한국어자바').rglob('*.java'))
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', ਸ੍ਰੇਣੀ_ਰਸਤਾ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(ਰੂਟ_ਰਸਤਾ / '한국어자바').with_suffix('.class')
        ਪੇਲੋਡ_ਸਮੱਗਰੀ = (ਸ੍ਰੇਣੀ_ਰਸਤਾ / 상대경로).read_bytes()
        ਨਾਂ = str(상대경로).replace('/', '.')
        if len(ਪੇਲੋਡ_ਸਮੱਗਰੀ) > 16384 or len(ਨਾਂ.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + ਨਾਂ)
        항목들.append((상대경로, ਨਾਂ, ਪੇਲੋਡ_ਸਮੱਗਰੀ))
    ਸਿਰਲੇਖ_ਕੀਮਤ = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *ਨਾਂ; const unsigned char *ਸਮੱਗਰੀ; unsigned ਆਕਾਰ; } 자바자원;']
    for 순번, (_, ਨਾਂ, ਪੇਲੋਡ_ਸਮੱਗਰੀ) in enumerate(항목들):
        ਸਿਰਲੇਖ_ਕੀਮਤ.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in ਪੇਲੋਡ_ਸਮੱਗਰੀ)))
    ਸਿਰਲੇਖ_ਕੀਮਤ.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, ਨਾਂ, ਪੇਲੋਡ_ਸਮੱਗਰੀ) in enumerate(항목들):
        ਸਿਰਲੇਖ_ਕੀਮਤ.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(ਨਾਂ, ensure_ascii=False), 순번, len(ਪੇਲੋਡ_ਸਮੱਗਰੀ)))
    ਸਿਰਲੇਖ_ਕੀਮਤ.append('};')
    (ਰੂਟ_ਰਸਤਾ / 'build/user/java-resources.h').write_text('\n'.join(ਸਿਰਲੇਖ_ਕੀਮਤ) + '\n', encoding='utf-8')
    배포경로 = ਰੂਟ_ਰਸਤਾ / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, ਪੇਲੋਡ_ਸਮੱਗਰੀ in 항목들:
            ਸਿਸਟਮ_ਜਾਣਕਾਰੀ = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); ਸਿਸਟਮ_ਜਾਣਕਾਰੀ.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(ਸਿਸਟਮ_ਜਾਣਕਾਰੀ, ਪੇਲੋਡ_ਸਮੱਗਰੀ)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as ਸੰਗ੍ਰਹਿ:
        for 원본주소 in 원문목록:
            ਸਿਸਟਮ_ਜਾਣਕਾਰੀ = zipfile.ZipInfo(str(원본주소.relative_to(ਰੂਟ_ਰਸਤਾ / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); ਸਿਸਟਮ_ਜਾਣਕਾਰੀ.compress_type = zipfile.ZIP_DEFLATED
            ਸੰਗ੍ਰਹਿ.writestr(ਸਿਸਟਮ_ਜਾਣਕਾਰੀ, 원본주소.read_bytes())
