"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 읽기 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(रूट_पाथ, पाळो_दिवचो_आदेश):
    (रूट_पाथ / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = रूट_पाथ / 'build/java-library'
    वर्ग_पाथ = 출력결과 / 'classes'
    वर्ग_पाथ.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((रूट_पाथ / '한국어자바').rglob('*.java'))
    पाळो_दिवचो_आदेश(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', वर्ग_पाथ] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(रूट_पाथ / '한국어자바').with_suffix('.class')
        पेलोड_डेटा = (वर्ग_पाथ / 상대경로).read_bytes()
        नांव = str(상대경로).replace('/', '.')
        if len(पेलोड_डेटा) > 16384 or len(नांव.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + नांव)
        항목들.append((상대경로, नांव, पेलोड_डेटा))
    माथाळो_मोल = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *नांव; const unsigned char *डेटा; unsigned आवाठ; } 자바자원;']
    for 순번, (_, नांव, पेलोड_डेटा) in enumerate(항목들):
        माथाळो_मोल.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_मोल) for SECOND_मोल in पेलोड_डेटा)))
    माथाळो_मोल.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, नांव, पेलोड_डेटा) in enumerate(항목들):
        माथाळो_मोल.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(नांव, ensure_ascii=False), 순번, len(पेलोड_डेटा)))
    माथाळो_मोल.append('};')
    (रूट_पाथ / 'build/user/java-resources.h').write_text('\n'.join(माथाळो_मोल) + '\n', encoding='utf-8')
    배포경로 = रूट_पाथ / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, पेलोड_डेटा in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, पेलोड_डेटा)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as संग्रह:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(रूट_पाथ / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            संग्रह.writestr(msinfo32_exe, 원본주소.read_bytes())
