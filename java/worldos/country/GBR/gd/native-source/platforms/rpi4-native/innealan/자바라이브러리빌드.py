"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 읽기 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(freumh_slighe, gnìomhaich_àithne):
    (freumh_slighe / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = freumh_slighe / 'build/java-library'
    clas_slighe = 출력결과 / 'classes'
    clas_slighe.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((freumh_slighe / '한국어자바').rglob('*.java'))
    gnìomhaich_àithne(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', clas_slighe] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(freumh_slighe / '한국어자바').with_suffix('.class')
        payload_dàta = (clas_slighe / 상대경로).read_bytes()
        Ainm = str(상대경로).replace('/', '.')
        if len(payload_dàta) > 16384 or len(Ainm.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Ainm)
        항목들.append((상대경로, Ainm, payload_dàta))
    bann_cinn_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Ainm; const unsigned char *dàta; unsigned atharraich_am_meud; } 자바자원;']
    for 순번, (_, Ainm, payload_dàta) in enumerate(항목들):
        bann_cinn_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in payload_dàta)))
    bann_cinn_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Ainm, payload_dàta) in enumerate(항목들):
        bann_cinn_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Ainm, ensure_ascii=False), 순번, len(payload_dàta)))
    bann_cinn_VALUE.append('};')
    (freumh_slighe / 'build/user/java-resources.h').write_text('\n'.join(bann_cinn_VALUE) + '\n', encoding='utf-8')
    배포경로 = freumh_slighe / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, payload_dàta in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, payload_dàta)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as taisg:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(freumh_slighe / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            taisg.writestr(msinfo32_exe, 원본주소.read_bytes())
