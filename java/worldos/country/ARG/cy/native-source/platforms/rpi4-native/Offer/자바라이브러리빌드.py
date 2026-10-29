"""자체 JVM용 Cymraeg class/JAR와 EL0에 넣을 Darllen 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(gwraidd_llwybr, Gweithredu_gorchymyn):
    (gwraidd_llwybr / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = gwraidd_llwybr / 'build/java-library'
    Dosbarth_llwybr = 출력결과 / 'classes'
    Dosbarth_llwybr.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((gwraidd_llwybr / '한국어자바').rglob('*.java'))
    Gweithredu_gorchymyn(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Dosbarth_llwybr] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(gwraidd_llwybr / '한국어자바').with_suffix('.class')
        llwyth_uchaf_data = (Dosbarth_llwybr / 상대경로).read_bytes()
        Enw = str(상대경로).replace('/', '.')
        if len(llwyth_uchaf_data) > 16384 or len(Enw.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Enw)
        항목들.append((상대경로, Enw, llwyth_uchaf_data))
    Pennyn_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Enw; const unsigned char *data; unsigned Maint; } 자바자원;']
    for 순번, (_, Enw, llwyth_uchaf_data) in enumerate(항목들):
        Pennyn_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in llwyth_uchaf_data)))
    Pennyn_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Enw, llwyth_uchaf_data) in enumerate(항목들):
        Pennyn_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Enw, ensure_ascii=False), 순번, len(llwyth_uchaf_data)))
    Pennyn_VALUE.append('};')
    (gwraidd_llwybr / 'build/user/java-resources.h').write_text('\n'.join(Pennyn_VALUE) + '\n', encoding='utf-8')
    배포경로 = gwraidd_llwybr / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, llwyth_uchaf_data in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, llwyth_uchaf_data)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Archif:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(gwraidd_llwybr / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Archif.writestr(msinfo32_exe, 원본주소.read_bytes())
