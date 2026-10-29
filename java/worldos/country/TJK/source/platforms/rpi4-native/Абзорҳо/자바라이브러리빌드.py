"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 Хондан 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(기준경로, иҷро_кардан_фармон):
    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = 기준경로 / 'build/java-library'
    синф_масир = 출력결과 / 'classes'
    синф_масир.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((기준경로 / '한국어자바').rglob('*.java'))
    иҷро_кардан_фармон(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', синф_масир] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(기준경로 / '한국어자바').with_suffix('.class')
        қобилият_иттилоот = (синф_масир / 상대경로).read_bytes()
        Ном = str(상대경로).replace('/', '.')
        if len(қобилият_иттилоот) > 16384 or len(Ном.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Ном)
        항목들.append((상대경로, Ном, қобилият_иттилоот))
    Сарнавор_қимат = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Ном; const unsigned char *иттилоот; unsigned андоза_кардан; } 자바자원;']
    for 순번, (_, Ном, қобилият_иттилоот) in enumerate(항목들):
        Сарнавор_қимат.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in қобилият_иттилоот)))
    Сарнавор_қимат.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Ном, қобилият_иттилоот) in enumerate(항목들):
        Сарнавор_қимат.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Ном, ensure_ascii=False), 순번, len(қобилият_иттилоот)))
    Сарнавор_қимат.append('};')
    (기준경로 / 'build/user/java-resources.h').write_text('\n'.join(Сарнавор_қимат) + '\n', encoding='utf-8')
    배포경로 = 기준경로 / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, қобилият_иттилоот in 항목들:
            Маълумоти_система = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); Маълумоти_система.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(Маълумоти_система, қобилият_иттилоот)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Бойгонӣ:
        for 원본주소 in 원문목록:
            Маълумоти_система = zipfile.ZipInfo(str(원본주소.relative_to(기준경로 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); Маълумоти_система.compress_type = zipfile.ZIP_DEFLATED
            Бойгонӣ.writestr(Маълумоти_система, 원본주소.read_bytes())
