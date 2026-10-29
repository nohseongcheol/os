"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 អាន 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(ឬស_ផ្លូវ, អនុវត្ត_ពាក្យបញ្ជា):
    (ឬស_ផ្លូវ / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = ឬស_ផ្លូវ / 'build/java-library'
    ថ្នាក់_ផ្លូវ = 출력결과 / 'classes'
    ថ្នាក់_ផ្លូវ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((ឬស_ផ្លូវ / '한국어자바').rglob('*.java'))
    អនុវត្ត_ពាក្យបញ្ជា(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', ថ្នាក់_ផ្លូវ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(ឬស_ផ្លូវ / '한국어자바').with_suffix('.class')
        ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ = (ថ្នាក់_ផ្លូវ / 상대경로).read_bytes()
        ឈ្មោះ = str(상대경로).replace('/', '.')
        if len(ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ) > 16384 or len(ឈ្មោះ.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + ឈ្មោះ)
        항목들.append((상대경로, ឈ្មោះ, ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ))
    បឋមកថា_តំលៃ = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *ឈ្មោះ; const unsigned char *ទិន្នន័យ; unsigned ដាក់ទំហំ; } 자바자원;']
    for 순번, (_, ឈ្មោះ, ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ) in enumerate(항목들):
        បឋមកថា_តំលៃ.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ)))
    បឋមកថា_តំលៃ.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, ឈ្មោះ, ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ) in enumerate(항목들):
        បឋមកថា_តំលៃ.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(ឈ្មោះ, ensure_ascii=False), 순번, len(ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ)))
    បឋមកថា_តំលៃ.append('};')
    (ឬស_ផ្លូវ / 'build/user/java-resources.h').write_text('\n'.join(បឋមកថា_តំលៃ) + '\n', encoding='utf-8')
    배포경로 = ឬស_ផ្លូវ / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ in 항목들:
            ប្រព័ន្ធព័ត៌មាន = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); ប្រព័ន្ធព័ត៌មាន.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(ប្រព័ន្ធព័ត៌មាន, ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as ប័ណ្ណសារ:
        for 원본주소 in 원문목록:
            ប្រព័ន្ធព័ត៌មាន = zipfile.ZipInfo(str(원본주소.relative_to(ឬស_ផ្លូវ / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); ប្រព័ន្ធព័ត៌មាន.compress_type = zipfile.ZIP_DEFLATED
            ប័ណ្ណសារ.writestr(ប្រព័ន្ធព័ត៌មាន, 원본주소.read_bytes())
