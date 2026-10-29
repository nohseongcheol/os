"""עצמי JVM용 עברית class/JAR와 EL0에 넣을 קרא 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(בסיס_נתיב, לבצע_פקודה):
    (בסיס_נתיב / 'build/user').mkdir(parents=True, exist_ok=True)
    פלט = בסיס_נתיב / 'build/java-library'
    כיתה_נתיב = פלט / 'classes'
    כיתה_נתיב.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((בסיס_נתיב / '한국어자바').rglob('*.java'))
    לבצע_פקודה(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', כיתה_נתיב] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        נתיב_יחסי = 원본주소.relative_to(בסיס_נתיב / '한국어자바').with_suffix('.class')
        מטען_נתונים = (כיתה_נתיב / נתיב_יחסי).read_bytes()
        שם = str(נתיב_יחסי).replace('/', '.')
        if len(מטען_נתונים) > 16384 or len(שם.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + שם)
        항목들.append((נתיב_יחסי, שם, מטען_נתונים))
    כותרת_ערך = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *שם; const unsigned char *נתונים; unsigned גודל; } 자바자원;']
    for 순번, (_, שם, מטען_נתונים) in enumerate(항목들):
        כותרת_ערך.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in מטען_נתונים)))
    כותרת_ערך.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, שם, מטען_נתונים) in enumerate(항목들):
        כותרת_ערך.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(שם, ensure_ascii=False), 순번, len(מטען_נתונים)))
    כותרת_ערך.append('};')
    (בסיס_נתיב / 'build/user/java-resources.h').write_text('\n'.join(כותרת_ערך) + '\n', encoding='utf-8')
    הפצה_נתיב = בסיס_נתיב / 'dist'; הפצה_נתיב.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(הפצה_נתיב / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for נתיב_יחסי, _, מטען_נתונים in 항목들:
            מידע_מערכת = zipfile.ZipInfo(str(נתיב_יחסי), date_time=(1980, 1, 1, 0, 0, 0)); מידע_מערכת.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(מידע_מערכת, מטען_נתונים)
    with zipfile.ZipFile(str(הפצה_נתיב / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as ארכיון:
        for 원본주소 in 원문목록:
            מידע_מערכת = zipfile.ZipInfo(str(원본주소.relative_to(בסיס_נתיב / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); מידע_מערכת.compress_type = zipfile.ZIP_DEFLATED
            ארכיון.writestr(מידע_מערכת, 원본주소.read_bytes())
