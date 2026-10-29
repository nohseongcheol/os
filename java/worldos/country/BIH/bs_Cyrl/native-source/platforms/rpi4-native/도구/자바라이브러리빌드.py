"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 읽기 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(기준경로, 실행):
    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = 기준경로 / 'build/java-library'
    класа_пут = 출력결과 / 'classes'
    класа_пут.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((기준경로 / '한국어자바').rglob('*.java'))
    실행(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', класа_пут] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(기준경로 / '한국어자바').with_suffix('.class')
        корисни_садржај_подаци = (класа_пут / 상대경로).read_bytes()
        назив = str(상대경로).replace('/', '.')
        if len(корисни_садржај_подаци) > 16384 or len(назив.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + назив)
        항목들.append((상대경로, назив, корисни_садржај_подаци))
    заглавље_вриједност = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *назив; const unsigned char *подаци; unsigned подесити_величину; } 자바자원;']
    for 순번, (_, назив, корисни_садржај_подаци) in enumerate(항목들):
        заглавље_вриједност.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in корисни_садржај_подаци)))
    заглавље_вриједност.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, назив, корисни_садржај_подаци) in enumerate(항목들):
        заглавље_вриједност.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(назив, ensure_ascii=False), 순번, len(корисни_садржај_подаци)))
    заглавље_вриједност.append('};')
    (기준경로 / 'build/user/java-resources.h').write_text('\n'.join(заглавље_вриједност) + '\n', encoding='utf-8')
    배포경로 = 기준경로 / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, корисни_садржај_подаци in 항목들:
            систем_информација = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); систем_информација.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(систем_информација, корисни_садржај_подаци)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as архива:
        for 원본주소 in 원문목록:
            систем_информација = zipfile.ZipInfo(str(원본주소.relative_to(기준경로 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); систем_информација.compress_type = zipfile.ZIP_DEFLATED
            архива.writestr(систем_информација, 원본주소.read_bytes())
