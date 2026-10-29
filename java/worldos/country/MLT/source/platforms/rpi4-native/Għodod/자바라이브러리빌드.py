"""자체 JVM용 Malti class/JAR와 EL0에 넣을 읽기 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(għerq_mogħdija, eżegwixxa_kmand):
    (għerq_mogħdija / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = għerq_mogħdija / 'build/java-library'
    klassi_mogħdija = 출력결과 / 'classes'
    klassi_mogħdija.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((għerq_mogħdija / '한국어자바').rglob('*.java'))
    eżegwixxa_kmand(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', klassi_mogħdija] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(għerq_mogħdija / '한국어자바').with_suffix('.class')
        payload_data = (klassi_mogħdija / 상대경로).read_bytes()
        isem = str(상대경로).replace('/', '.')
        if len(payload_data) > 16384 or len(isem.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + isem)
        항목들.append((상대경로, isem, payload_data))
    Intestazzjoni_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *isem; const unsigned char *data; unsigned daqqas; } 자바자원;']
    for 순번, (_, isem, payload_data) in enumerate(항목들):
        Intestazzjoni_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in payload_data)))
    Intestazzjoni_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, isem, payload_data) in enumerate(항목들):
        Intestazzjoni_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(isem, ensure_ascii=False), 순번, len(payload_data)))
    Intestazzjoni_VALUE.append('};')
    (għerq_mogħdija / 'build/user/java-resources.h').write_text('\n'.join(Intestazzjoni_VALUE) + '\n', encoding='utf-8')
    배포경로 = għerq_mogħdija / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, payload_data in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, payload_data)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arkivju:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(għerq_mogħdija / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arkivju.writestr(msinfo32_exe, 원본주소.read_bytes())
