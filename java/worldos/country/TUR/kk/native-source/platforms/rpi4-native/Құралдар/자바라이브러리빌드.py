"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 Оқу 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(түбір_жол, орындау_пәрмен):
    (түбір_жол / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = түбір_жол / 'build/java-library'
    оқу_жол = 출력결과 / 'classes'
    оқу_жол.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((түбір_жол / '한국어자바').rglob('*.java'))
    орындау_пәрмен(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', оқу_жол] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(түбір_жол / '한국어자바').with_suffix('.class')
        жүктеме_деректер = (оқу_жол / 상대경로).read_bytes()
        Аты = str(상대경로).replace('/', '.')
        if len(жүктеме_деректер) > 16384 or len(Аты.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Аты)
        항목들.append((상대경로, Аты, жүктеме_деректер))
    Тақырып_мән = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Аты; const unsigned char *деректер; unsigned Өлшемі; } 자바자원;']
    for 순번, (_, Аты, жүктеме_деректер) in enumerate(항목들):
        Тақырып_мән.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in жүктеме_деректер)))
    Тақырып_мән.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Аты, жүктеме_деректер) in enumerate(항목들):
        Тақырып_мән.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Аты, ensure_ascii=False), 순번, len(жүктеме_деректер)))
    Тақырып_мән.append('};')
    (түбір_жол / 'build/user/java-resources.h').write_text('\n'.join(Тақырып_мән) + '\n', encoding='utf-8')
    배포경로 = түбір_жол / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, жүктеме_деректер in 항목들:
            Жүйелік_ақпарат = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); Жүйелік_ақпарат.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(Жүйелік_ақпарат, жүктеме_деректер)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Мұрағат:
        for 원본주소 in 원문목록:
            Жүйелік_ақпарат = zipfile.ZipInfo(str(원본주소.relative_to(түбір_жол / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); Жүйелік_ақпарат.compress_type = zipfile.ZIP_DEFLATED
            Мұрағат.writestr(Жүйелік_ақпарат, 원본주소.read_bytes())
