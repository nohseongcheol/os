"""자체 JVM용 ಕನ್ನಡ class/JAR와 EL0에 넣을 ಓದು 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(ಮೂಲ_ಹಾದಿ, ಪೂರೈಸು_ಆದೇಶ):
    (ಮೂಲ_ಹಾದಿ / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = ಮೂಲ_ಹಾದಿ / 'build/java-library'
    ವರ್ಗ_ಹಾದಿ = 출력결과 / 'classes'
    ವರ್ಗ_ಹಾದಿ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((ಮೂಲ_ಹಾದಿ / '한국어자바').rglob('*.java'))
    ಪೂರೈಸು_ಆದೇಶ(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', ವರ್ಗ_ಹಾದಿ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(ಮೂಲ_ಹಾದಿ / '한국어자바').with_suffix('.class')
        ಪೇಲೋಡ್_ಡೇಟಾ = (ವರ್ಗ_ಹಾದಿ / 상대경로).read_bytes()
        ಹೆಸರು = str(상대경로).replace('/', '.')
        if len(ಪೇಲೋಡ್_ಡೇಟಾ) > 16384 or len(ಹೆಸರು.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + ಹೆಸರು)
        항목들.append((상대경로, ಹೆಸರು, ಪೇಲೋಡ್_ಡೇಟಾ))
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *ಹೆಸರು; const unsigned char *ಡೇಟಾ; unsigned ಗಾತ್ರ; } 자바자원;']
    for 순번, (_, ಹೆಸರು, ಪೇಲೋಡ್_ಡೇಟಾ) in enumerate(항목들):
        ಶಿರೋಲೇಖ_ಮೌಲ್ಯ.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in ಪೇಲೋಡ್_ಡೇಟಾ)))
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, ಹೆಸರು, ಪೇಲೋಡ್_ಡೇಟಾ) in enumerate(항목들):
        ಶಿರೋಲೇಖ_ಮೌಲ್ಯ.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(ಹೆಸರು, ensure_ascii=False), 순번, len(ಪೇಲೋಡ್_ಡೇಟಾ)))
    ಶಿರೋಲೇಖ_ಮೌಲ್ಯ.append('};')
    (ಮೂಲ_ಹಾದಿ / 'build/user/java-resources.h').write_text('\n'.join(ಶಿರೋಲೇಖ_ಮೌಲ್ಯ) + '\n', encoding='utf-8')
    배포경로 = ಮೂಲ_ಹಾದಿ / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, ಪೇಲೋಡ್_ಡೇಟಾ in 항목들:
            ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ, ಪೇಲೋಡ್_ಡೇಟಾ)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as ಅರ್ಖೀವ್:
        for 원본주소 in 원문목록:
            ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ = zipfile.ZipInfo(str(원본주소.relative_to(ಮೂಲ_ಹಾದಿ / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ.compress_type = zipfile.ZIP_DEFLATED
            ಅರ್ಖೀವ್.writestr(ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ, 원본주소.read_bytes())
