"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 Leximi 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(rrënjë_shteg, zbatoj_komandë):
    (rrënjë_shteg / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = rrënjë_shteg / 'build/java-library'
    klasë_shteg = 출력결과 / 'classes'
    klasë_shteg.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((rrënjë_shteg / '한국어자바').rglob('*.java'))
    zbatoj_komandë(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', klasë_shteg] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        상대경로 = 원본주소.relative_to(rrënjë_shteg / '한국어자바').with_suffix('.class')
        ngarkesë_e_dobishme_të_dhëna = (klasë_shteg / 상대경로).read_bytes()
        Emër = str(상대경로).replace('/', '.')
        if len(ngarkesë_e_dobishme_të_dhëna) > 16384 or len(Emër.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Emër)
        항목들.append((상대경로, Emër, ngarkesë_e_dobishme_të_dhëna))
    Kreu_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Emër; const unsigned char *të_dhëna; unsigned Madhësi; } 자바자원;']
    for 순번, (_, Emër, ngarkesë_e_dobishme_të_dhëna) in enumerate(항목들):
        Kreu_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in ngarkesë_e_dobishme_të_dhëna)))
    Kreu_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Emër, ngarkesë_e_dobishme_të_dhëna) in enumerate(항목들):
        Kreu_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Emër, ensure_ascii=False), 순번, len(ngarkesë_e_dobishme_të_dhëna)))
    Kreu_VALUE.append('};')
    (rrënjë_shteg / 'build/user/java-resources.h').write_text('\n'.join(Kreu_VALUE) + '\n', encoding='utf-8')
    배포경로 = rrënjë_shteg / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for 상대경로, _, ngarkesë_e_dobishme_të_dhëna in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(상대경로), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, ngarkesë_e_dobishme_të_dhëna)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as arkiv:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(rrënjë_shteg / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            arkiv.writestr(msinfo32_exe, 원본주소.read_bytes())
