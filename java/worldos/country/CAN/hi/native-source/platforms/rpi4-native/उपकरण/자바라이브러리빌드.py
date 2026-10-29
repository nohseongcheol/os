"""निज JVM용 हिंदी class/JAR와 EL0에 넣을 पढ़ें 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(मूल_पथ, निष्पादित_करें_आदेश):
    (मूल_पथ / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = मूल_पथ / 'build/java-library'
    कक्षा_पथ = 출력결과 / 'classes'
    कक्षा_पथ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((मूल_पथ / '한국어자바').rglob('*.java'))
    निष्पादित_करें_आदेश(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', कक्षा_पथ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        संबंधित_पथ = 원본주소.relative_to(मूल_पथ / '한국어자바').with_suffix('.class')
        पेलोड_डेटा = (कक्षा_पथ / संबंधित_पथ).read_bytes()
        नाम = str(संबंधित_पथ).replace('/', '.')
        if len(पेलोड_डेटा) > 16384 or len(नाम.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + नाम)
        항목들.append((संबंधित_पथ, नाम, पेलोड_डेटा))
    हेडर_मान = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *नाम; const unsigned char *आँकड़े; unsigned आकार; } 자바자원;']
    for 순번, (_, नाम, पेलोड_डेटा) in enumerate(항목들):
        हेडर_मान.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in पेलोड_डेटा)))
    हेडर_मान.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, नाम, पेलोड_डेटा) in enumerate(항목들):
        हेडर_मान.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(नाम, ensure_ascii=False), 순번, len(पेलोड_डेटा)))
    हेडर_मान.append('};')
    (मूल_पथ / 'build/user/java-resources.h').write_text('\n'.join(हेडर_मान) + '\n', encoding='utf-8')
    배포경로 = मूल_पथ / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for संबंधित_पथ, _, पेलोड_डेटा in 항목들:
            सिस्टम_जानकारी = zipfile.ZipInfo(str(संबंधित_पथ), date_time=(1980, 1, 1, 0, 0, 0)); सिस्टम_जानकारी.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(सिस्टम_जानकारी, पेलोड_डेटा)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as संग्रह:
        for 원본주소 in 원문목록:
            सिस्टम_जानकारी = zipfile.ZipInfo(str(원본주소.relative_to(मूल_पथ / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); सिस्टम_जानकारी.compress_type = zipfile.ZIP_DEFLATED
            संग्रह.writestr(सिस्टम_जानकारी, 원본주소.read_bytes())
