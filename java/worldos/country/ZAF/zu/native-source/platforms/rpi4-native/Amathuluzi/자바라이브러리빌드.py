"""자체 JVM용 Isi_Zulu class/JAR와 EL0에 넣을 Funda 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(기준경로, yenza_umyalo):
    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = 기준경로 / 'build/java-library'
    uhlobo_umzila = 출력결과 / 'classes'
    uhlobo_umzila.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((기준경로 / '한국어자바').rglob('*.java'))
    yenza_umyalo(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', uhlobo_umzila] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(기준경로 / '한국어자바').with_suffix('.class')
        ukulayisha_okukhokhelwayo_imininingwane = (uhlobo_umzila / 상대경로).read_bytes()
        Igama = str(상대경로).replace('/', '.')
        if len(ukulayisha_okukhokhelwayo_imininingwane) > 16384 or len(Igama.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Igama)
        항목들.append((상대경로, Igama, ukulayisha_okukhokhelwayo_imininingwane))
    Unhlokweni_inani = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Igama; const unsigned char *imininingwane; unsigned Ubungako; } 자바자원;']
    for 순번, (_, Igama, ukulayisha_okukhokhelwayo_imininingwane) in enumerate(항목들):
        Unhlokweni_inani.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(둘째값) for 둘째값 in ukulayisha_okukhokhelwayo_imininingwane)))
    Unhlokweni_inani.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Igama, ukulayisha_okukhokhelwayo_imininingwane) in enumerate(항목들):
        Unhlokweni_inani.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Igama, ensure_ascii=False), 순번, len(ukulayisha_okukhokhelwayo_imininingwane)))
    Unhlokweni_inani.append('};')
    (기준경로 / 'build/user/java-resources.h').write_text('\n'.join(Unhlokweni_inani) + '\n', encoding='utf-8')
    배포경로 = 기준경로 / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, ukulayisha_okukhokhelwayo_imininingwane in 항목들:
            I_msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); I_msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(I_msinfo32_exe, ukulayisha_okukhokhelwayo_imininingwane)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as londoloza:
        for 원본주소 in 원문목록:
            I_msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(기준경로 / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); I_msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            londoloza.writestr(I_msinfo32_exe, 원본주소.read_bytes())
