"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 კითხვა 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(ფესვი_მდებარეობა, შესრულება_ბრძანება):
    (ფესვი_მდებარეობა / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = ფესვი_მდებარეობა / 'build/java-library'
    კლასი_მდებარეობა = 출력결과 / 'classes'
    კლასი_მდებარეობა.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((ფესვი_მდებარეობა / '한국어자바').rglob('*.java'))
    შესრულება_ბრძანება(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', კლასი_მდებარეობა] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(ფესვი_მდებარეობა / '한국어자바').with_suffix('.class')
        დატვირთვა_მონაცემები = (კლასი_მდებარეობა / 상대경로).read_bytes()
        სახელი = str(상대경로).replace('/', '.')
        if len(დატვირთვა_მონაცემები) > 16384 or len(სახელი.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + სახელი)
        항목들.append((상대경로, სახელი, დატვირთვა_მონაცემები))
    ზედა_კოლონტიტული_მნიშვნელობა = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *სახელი; const unsigned char *მონაცემები; unsigned ზომა; } 자바자원;']
    for 순번, (_, სახელი, დატვირთვა_მონაცემები) in enumerate(항목들):
        ზედა_კოლონტიტული_მნიშვნელობა.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in დატვირთვა_მონაცემები)))
    ზედა_კოლონტიტული_მნიშვნელობა.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, სახელი, დატვირთვა_მონაცემები) in enumerate(항목들):
        ზედა_კოლონტიტული_მნიშვნელობა.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(სახელი, ensure_ascii=False), 순번, len(დატვირთვა_მონაცემები)))
    ზედა_კოლონტიტული_მნიშვნელობა.append('};')
    (ფესვი_მდებარეობა / 'build/user/java-resources.h').write_text('\n'.join(ზედა_კოლონტიტული_მნიშვნელობა) + '\n', encoding='utf-8')
    배포경로 = ფესვი_მდებარეობა / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, დატვირთვა_მონაცემები in 항목들:
            სისტემის_ინფორმაცია = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); სისტემის_ინფორმაცია.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(სისტემის_ინფორმაცია, დატვირთვა_მონაცემები)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as არქივი:
        for 원본주소 in 원문목록:
            სისტემის_ინფორმაცია = zipfile.ZipInfo(str(원본주소.relative_to(ფესვი_მდებარეობა / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); სისტემის_ინფორმაცია.compress_type = zipfile.ZIP_DEFLATED
            არქივი.writestr(სისტემის_ინფორმაცია, 원본주소.read_bytes())
