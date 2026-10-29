"""निज JVM용 नेपाली class/JAR와 EL0에 넣을 पढनुहोस् 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(रूट_बाटो, कार्यान्वयन_गर्नुहोस्_आदेश):
    (रूट_बाटो / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = रूट_बाटो / 'build/java-library'
    वर्ग_बाटो = 출력결과 / 'classes'
    वर्ग_बाटो.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((रूट_बाटो / '한국어자바').rglob('*.java'))
    कार्यान्वयन_गर्नुहोस्_आदेश(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', वर्ग_बाटो] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(रूट_बाटो / '한국어자바').with_suffix('.class')
        पेलोड_लगत = (वर्ग_बाटो / 상대경로).read_bytes()
        नाम = str(상대경로).replace('/', '.')
        if len(पेलोड_लगत) > 16384 or len(नाम.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + नाम)
        항목들.append((상대경로, नाम, पेलोड_लगत))
    हेडर_मान = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *नाम; const unsigned char *लगत; unsigned आकार; } 자바자원;']
    for 순번, (_, नाम, पेलोड_लगत) in enumerate(항목들):
        हेडर_मान.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in पेलोड_लगत)))
    हेडर_मान.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, नाम, पेलोड_लगत) in enumerate(항목들):
        हेडर_मान.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(नाम, ensure_ascii=False), 순번, len(पेलोड_लगत)))
    हेडर_मान.append('};')
    (रूट_बाटो / 'build/user/java-resources.h').write_text('\n'.join(हेडर_मान) + '\n', encoding='utf-8')
    배포경로 = रूट_बाटो / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, पेलोड_लगत in 항목들:
            प्रणाली_जानकारी = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); प्रणाली_जानकारी.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(प्रणाली_जानकारी, पेलोड_लगत)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as सङ्ग्रह:
        for 원본주소 in 원문목록:
            प्रणाली_जानकारी = zipfile.ZipInfo(str(원본주소.relative_to(रूट_बाटो / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); प्रणाली_जानकारी.compress_type = zipfile.ZIP_DEFLATED
            सङ्ग्रह.writestr(प्रणाली_जानकारी, 원본주소.read_bytes())
