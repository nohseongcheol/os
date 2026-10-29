"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 ئوقۇ 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(يىلتىز_يول, ئىجرا_قىلىش_بۇيرۇق):
    (يىلتىز_يول / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = يىلتىز_يول / 'build/java-library'
    تۈركۈم_يول = 출력결과 / 'classes'
    تۈركۈم_يول.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((يىلتىز_يول / '한국어자바').rglob('*.java'))
    ئىجرا_قىلىش_بۇيرۇق(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', تۈركۈم_يول] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(يىلتىز_يول / '한국어자바').with_suffix('.class')
        يۈك_مەلۇمات = (تۈركۈم_يول / 상대경로).read_bytes()
        ئاتى = str(상대경로).replace('/', '.')
        if len(يۈك_مەلۇمات) > 16384 or len(ئاتى.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + ئاتى)
        항목들.append((상대경로, ئاتى, يۈك_مەلۇمات))
    بېشى_قىممىتى = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *ئاتى; const unsigned char *مەلۇمات; unsigned چوڭلۇقى; } 자바자원;']
    for 순번, (_, ئاتى, يۈك_مەلۇمات) in enumerate(항목들):
        بېشى_قىممىتى.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in يۈك_مەلۇمات)))
    بېشى_قىممىتى.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, ئاتى, يۈك_مەلۇمات) in enumerate(항목들):
        بېشى_قىممىتى.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(ئاتى, ensure_ascii=False), 순번, len(يۈك_مەلۇمات)))
    بېشى_قىممىتى.append('};')
    (يىلتىز_يول / 'build/user/java-resources.h').write_text('\n'.join(بېشى_قىممىتى) + '\n', encoding='utf-8')
    배포경로 = يىلتىز_يول / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, يۈك_مەلۇمات in 항목들:
            سىستېما_ئۇچۇرى = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); سىستېما_ئۇچۇرى.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(سىستېما_ئۇچۇرى, يۈك_مەلۇمات)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as ئارخىپ:
        for 원본주소 in 원문목록:
            سىستېما_ئۇچۇرى = zipfile.ZipInfo(str(원본주소.relative_to(يىلتىز_يول / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); سىستېما_ئۇچۇرى.compress_type = zipfile.ZIP_DEFLATED
            ئارخىپ.writestr(سىستېما_ئۇچۇرى, 원본주소.read_bytes())
