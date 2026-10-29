"""자체 JVM용 தமிழ் class/JAR와 EL0에 넣을 படி 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(மூலம்_பாதை, இயக்கு_கட்டளை):
    (மூலம்_பாதை / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = மூலம்_பாதை / 'build/java-library'
    பிரிவு_பாதை = 출력결과 / 'classes'
    பிரிவு_பாதை.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((மூலம்_பாதை / '한국어자바').rglob('*.java'))
    இயக்கு_கட்டளை(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', பிரிவு_பாதை] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        தொடர்புடைய_பாதை = 원본주소.relative_to(மூலம்_பாதை / '한국어자바').with_suffix('.class')
        பேலோட்_தரவு = (பிரிவு_பாதை / தொடர்புடைய_பாதை).read_bytes()
        பெயர் = str(தொடர்புடைய_பாதை).replace('/', '.')
        if len(பேலோட்_தரவு) > 16384 or len(பெயர்.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + பெயர்)
        항목들.append((தொடர்புடைய_பாதை, பெயர், பேலோட்_தரவு))
    மேற்குறிப்பு_மதிப்பு = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *பெயர்; const unsigned char *தரவு; unsigned அளவு; } 자바자원;']
    for 순번, (_, பெயர், பேலோட்_தரவு) in enumerate(항목들):
        மேற்குறிப்பு_மதிப்பு.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in பேலோட்_தரவு)))
    மேற்குறிப்பு_மதிப்பு.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, பெயர், பேலோட்_தரவு) in enumerate(항목들):
        மேற்குறிப்பு_மதிப்பு.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(பெயர், ensure_ascii=False), 순번, len(பேலோட்_தரவு)))
    மேற்குறிப்பு_மதிப்பு.append('};')
    (மூலம்_பாதை / 'build/user/java-resources.h').write_text('\n'.join(மேற்குறிப்பு_மதிப்பு) + '\n', encoding='utf-8')
    배포경로 = மூலம்_பாதை / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for தொடர்புடைய_பாதை, _, பேலோட்_தரவு in 항목들:
            கணினித்_தகவல் = zipfile.ZipInfo(str(தொடர்புடைய_பாதை), date_time=(1980, 1, 1, 0, 0, 0)); கணினித்_தகவல்.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(கணினித்_தகவல், பேலோட்_தரவு)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as காப்பகம்:
        for 원본주소 in 원문목록:
            கணினித்_தகவல் = zipfile.ZipInfo(str(원본주소.relative_to(மூலம்_பாதை / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); கணினித்_தகவல்.compress_type = zipfile.ZIP_DEFLATED
            காப்பகம்.writestr(கணினித்_தகவல், 원본주소.read_bytes())
