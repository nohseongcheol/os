"""자체 JVM용 አማርኛ class/JAR와 EL0에 넣을 ማንበቢያ 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(ስር_ዱካ, ፈጽም_ትእዛዝ):
    (ስር_ዱካ / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = ስር_ዱካ / 'build/java-library'
    መደብ_ዱካ = 출력결과 / 'classes'
    መደብ_ዱካ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((ስር_ዱካ / '한국어자바').rglob('*.java'))
    ፈጽም_ትእዛዝ(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', መደብ_ዱካ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(ስር_ዱካ / '한국어자바').with_suffix('.class')
        የክፍያ_ጫና_ውሂብ = (መደብ_ዱካ / 상대경로).read_bytes()
        ስም = str(상대경로).replace('/', '.')
        if len(የክፍያ_ጫና_ውሂብ) > 16384 or len(ስም.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + ስም)
        항목들.append((상대경로, ስም, የክፍያ_ጫና_ውሂብ))
    ርእስ_እሴት = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *ስም; const unsigned char *ውሂብ; unsigned መጠን; } 자바자원;']
    for 순번, (_, ስም, የክፍያ_ጫና_ውሂብ) in enumerate(항목들):
        ርእስ_እሴት.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in የክፍያ_ጫና_ውሂብ)))
    ርእስ_እሴት.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, ስም, የክፍያ_ጫና_ውሂብ) in enumerate(항목들):
        ርእስ_እሴት.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(ስም, ensure_ascii=False), 순번, len(የክፍያ_ጫና_ውሂብ)))
    ርእስ_እሴት.append('};')
    (ስር_ዱካ / 'build/user/java-resources.h').write_text('\n'.join(ርእስ_እሴት) + '\n', encoding='utf-8')
    배포경로 = ስር_ዱካ / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, የክፍያ_ጫና_ውሂብ in 항목들:
            የስርዓት_መረጃ = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); የስርዓት_መረጃ.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(የስርዓት_መረጃ, የክፍያ_ጫና_ውሂብ)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as ከዝን:
        for 원본주소 in 원문목록:
            የስርዓት_መረጃ = zipfile.ZipInfo(str(원본주소.relative_to(ስር_ዱካ / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); የስርዓት_መረጃ.compress_type = zipfile.ZIP_DEFLATED
            ከዝን.writestr(የስርዓት_መረጃ, 원본주소.read_bytes())
