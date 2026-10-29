"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 വായന 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(വർഗ്ഗമൂലം_പാത, നടപ്പാക്കുക_കമാന്_ഡ്):
    (വർഗ്ഗമൂലം_പാത / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = വർഗ്ഗമൂലം_പാത / 'build/java-library'
    ക്ലാസ്_പാത = 출력결과 / 'classes'
    ക്ലാസ്_പാത.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((വർഗ്ഗമൂലം_പാത / '한국어자바').rglob('*.java'))
    നടപ്പാക്കുക_കമാന്_ഡ്(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', ക്ലാസ്_പാത] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        ആപേക്ഷിക_പാത = 원본주소.relative_to(വർഗ്ഗമൂലം_പാത / '한국어자바').with_suffix('.class')
        പേലോഡ്_ഡാറ്റാ = (ക്ലാസ്_പാത / ആപേക്ഷിക_പാത).read_bytes()
        പേരു് = str(ആപേക്ഷിക_പാത).replace('/', '.')
        if len(പേലോഡ്_ഡാറ്റാ) > 16384 or len(പേരു്.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + പേരു്)
        항목들.append((ആപേക്ഷിക_പാത, പേരു്, പേലോഡ്_ഡാറ്റാ))
    ശീർഷകം_മൂല്യം = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *പേരു്; const unsigned char *ഡാറ്റാ; unsigned വലിപ്പം; } 자바자원;']
    for 순번, (_, പേരു്, പേലോഡ്_ഡാറ്റാ) in enumerate(항목들):
        ശീർഷകം_മൂല്യം.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in പേലോഡ്_ഡാറ്റാ)))
    ശീർഷകം_മൂല്യം.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, പേരു്, പേലോഡ്_ഡാറ്റാ) in enumerate(항목들):
        ശീർഷകം_മൂല്യം.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(പേരു്, ensure_ascii=False), 순번, len(പേലോഡ്_ഡാറ്റാ)))
    ശീർഷകം_മൂല്യം.append('};')
    (വർഗ്ഗമൂലം_പാത / 'build/user/java-resources.h').write_text('\n'.join(ശീർഷകം_മൂല്യം) + '\n', encoding='utf-8')
    배포경로 = വർഗ്ഗമൂലം_പാത / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for ആപേക്ഷിക_പാത, _, പേലോഡ്_ഡാറ്റാ in 항목들:
            സിസ്റ്റം_വിവരങ്ങള് = zipfile.ZipInfo(str(ആപേക്ഷിക_പാത), date_time=(1980, 1, 1, 0, 0, 0)); സിസ്റ്റം_വിവരങ്ങള്.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(സിസ്റ്റം_വിവരങ്ങള്, പേലോഡ്_ഡാറ്റാ)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as ശേഖരം:
        for 원본주소 in 원문목록:
            സിസ്റ്റം_വിവരങ്ങള് = zipfile.ZipInfo(str(원본주소.relative_to(വർഗ്ഗമൂലം_പാത / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); സിസ്റ്റം_വിവരങ്ങള്.compress_type = zipfile.ZIP_DEFLATED
            ശേഖരം.writestr(സിസ്റ്റം_വിവരങ്ങള്, 원본주소.read_bytes())
