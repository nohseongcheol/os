"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 ପଢନ୍ତୁ 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(ରୁଟ୍_ପଥ, ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ):
    (ରୁଟ୍_ପଥ / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = ରୁଟ୍_ପଥ / 'build/java-library'
    ଶ୍ରେଣୀ_ପଥ = 출력결과 / 'classes'
    ଶ୍ରେଣୀ_ପଥ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((ରୁଟ୍_ପଥ / '한국어자바').rglob('*.java'))
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', ଶ୍ରେଣୀ_ପଥ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(ରୁଟ୍_ପଥ / '한국어자바').with_suffix('.class')
        ପେଲୋଡ୍_ଡାଟା = (ଶ୍ରେଣୀ_ପଥ / 상대경로).read_bytes()
        ନାମ = str(상대경로).replace('/', '.')
        if len(ପେଲୋଡ୍_ଡାଟା) > 16384 or len(ନାମ.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + ନାମ)
        항목들.append((상대경로, ନାମ, ପେଲୋଡ୍_ଡାଟା))
    ଶୀର୍ଷକ_ମୂଲ୍ୟ = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *ନାମ; const unsigned char *ଡାଟା; unsigned ଆକାର; } 자바자원;']
    for 순번, (_, ନାମ, ପେଲୋଡ୍_ଡାଟା) in enumerate(항목들):
        ଶୀର୍ଷକ_ମୂଲ୍ୟ.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in ପେଲୋଡ୍_ଡାଟା)))
    ଶୀର୍ଷକ_ମୂଲ୍ୟ.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, ନାମ, ପେଲୋଡ୍_ଡାଟା) in enumerate(항목들):
        ଶୀର୍ଷକ_ମୂଲ୍ୟ.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(ନାମ, ensure_ascii=False), 순번, len(ପେଲୋଡ୍_ଡାଟା)))
    ଶୀର୍ଷକ_ମୂଲ୍ୟ.append('};')
    (ରୁଟ୍_ପଥ / 'build/user/java-resources.h').write_text('\n'.join(ଶୀର୍ଷକ_ମୂଲ୍ୟ) + '\n', encoding='utf-8')
    배포경로 = ରୁଟ୍_ପଥ / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, ପେଲୋଡ୍_ଡାଟା in 항목들:
            ସିଷ୍ଟମ୍_ସୂଚନା = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); ସିଷ୍ଟମ୍_ସୂଚନା.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(ସିଷ୍ଟମ୍_ସୂଚନା, ପେଲୋଡ୍_ଡାଟା)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as ଅଭିଲେଖାଗାର:
        for 원본주소 in 원문목록:
            ସିଷ୍ଟମ୍_ସୂଚନା = zipfile.ZipInfo(str(원본주소.relative_to(ରୁଟ୍_ପଥ / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); ସିଷ୍ଟମ୍_ସୂଚନା.compress_type = zipfile.ZIP_DEFLATED
            ଅଭିଲେଖାଗାର.writestr(ସିଷ୍ଟମ୍_ସୂଚନା, 원본주소.read_bytes())
