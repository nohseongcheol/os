"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 Wepụta_ọzi 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(기준경로, mee_nnyemiwu):
    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = 기준경로 / 'build/java-library'
    klaàsị_ụzọ_ozi = 출력결과 / 'classes'
    klaàsị_ụzọ_ozi.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((기준경로 / '한국어자바').rglob('*.java'))
    mee_nnyemiwu(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', klaàsị_ụzọ_ozi] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(기준경로 / '한국어자바').with_suffix('.class')
        ebe_mbulingwa_datà = (klaàsị_ụzọ_ozi / 상대경로).read_bytes()
        Aha = str(상대경로).replace('/', '.')
        if len(ebe_mbulingwa_datà) > 16384 or len(Aha.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Aha)
        항목들.append((상대경로, Aha, ebe_mbulingwa_datà))
    isi_valuu = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Aha; const unsigned char *datà; unsigned Ụhara; } 자바자원;']
    for 순번, (_, Aha, ebe_mbulingwa_datà) in enumerate(항목들):
        isi_valuu.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in ebe_mbulingwa_datà)))
    isi_valuu.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Aha, ebe_mbulingwa_datà) in enumerate(항목들):
        isi_valuu.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Aha, ensure_ascii=False), 순번, len(ebe_mbulingwa_datà)))
    isi_valuu.append('};')
    (기준경로 / 'build/user/java-resources.h').write_text('\n'.join(isi_valuu) + '\n', encoding='utf-8')
    배포경로 = 기준경로 / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, ebe_mbulingwa_datà in 항목들:
            Ozi_Sistèm = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); Ozi_Sistèm.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(Ozi_Sistèm, ebe_mbulingwa_datà)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as ọkpụ:
        for 원본주소 in 원문목록:
            Ozi_Sistèm = zipfile.ZipInfo(str(원본주소.relative_to(기준경로 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); Ozi_Sistèm.compress_type = zipfile.ZIP_DEFLATED
            ọkpụ.writestr(Ozi_Sistèm, 원본주소.read_bytes())
