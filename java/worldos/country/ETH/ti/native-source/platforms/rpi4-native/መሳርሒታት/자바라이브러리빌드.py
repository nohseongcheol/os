"""자체 JVM용 ትግርኛ class/JAR와 EL0에 넣을 읽기 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(기준경로, ተግብር_ትእዛዝ):
    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = 기준경로 / 'build/java-library'
    ክፍሊ_መገዲ = 출력결과 / 'classes'
    ክፍሊ_መገዲ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((기준경로 / '한국어자바').rglob('*.java'))
    ተግብር_ትእዛዝ(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', ክፍሊ_መገዲ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(기준경로 / '한국어자바').with_suffix('.class')
        ጽዕነት_ክፍሊት_ሓበሬታ = (ክፍሊ_መገዲ / 상대경로).read_bytes()
        ሽም = str(상대경로).replace('/', '.')
        if len(ጽዕነት_ክፍሊት_ሓበሬታ) > 16384 or len(ሽም.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + ሽም)
        항목들.append((상대경로, ሽም, ጽዕነት_ክፍሊት_ሓበሬታ))
    ርእሲ_ዋጋ = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *ሽም; const unsigned char *ሓበሬታ; unsigned መጠን; } 자바자원;']
    for 순번, (_, ሽም, ጽዕነት_ክፍሊት_ሓበሬታ) in enumerate(항목들):
        ርእሲ_ዋጋ.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in ጽዕነት_ክፍሊት_ሓበሬታ)))
    ርእሲ_ዋጋ.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, ሽም, ጽዕነት_ክፍሊት_ሓበሬታ) in enumerate(항목들):
        ርእሲ_ዋጋ.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(ሽም, ensure_ascii=False), 순번, len(ጽዕነት_ክፍሊት_ሓበሬታ)))
    ርእሲ_ዋጋ.append('};')
    (기준경로 / 'build/user/java-resources.h').write_text('\n'.join(ርእሲ_ዋጋ) + '\n', encoding='utf-8')
    배포경로 = 기준경로 / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, ጽዕነት_ክፍሊት_ሓበሬታ in 항목들:
            ናይ_ስርዓት_ሓበሬታ = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); ናይ_ስርዓት_ሓበሬታ.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(ናይ_ስርዓት_ሓበሬታ, ጽዕነት_ክፍሊት_ሓበሬታ)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as ሰንድ:
        for 원본주소 in 원문목록:
            ናይ_ስርዓት_ሓበሬታ = zipfile.ZipInfo(str(원본주소.relative_to(기준경로 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); ናይ_ስርዓት_ሓበሬታ.compress_type = zipfile.ZIP_DEFLATED
            ሰንድ.writestr(ናይ_ስርዓት_ሓበሬታ, 원본주소.read_bytes())
