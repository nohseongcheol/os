"""eget JVM용 Svenska class/JAR와 EL0에 넣을 Läs 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(rot_väg, köra_kommando):
    (rot_väg / 'build/user').mkdir(parents=True, exist_ok=True)
    utleverans = rot_väg / 'build/java-library'
    Kurs_väg = utleverans / 'classes'
    Kurs_väg.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((rot_väg / '한국어자바').rglob('*.java'))
    köra_kommando(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Kurs_väg] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        relativ_sökväg = 원본주소.relative_to(rot_väg / '한국어자바').with_suffix('.class')
        nyttolast_data = (Kurs_väg / relativ_sökväg).read_bytes()
        Namn = str(relativ_sökväg).replace('/', '.')
        if len(nyttolast_data) > 16384 or len(Namn.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Namn)
        항목들.append((relativ_sökväg, Namn, nyttolast_data))
    huvud_värde = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Namn; const unsigned char *data; unsigned Storlek; } 자바자원;']
    for 순번, (_, Namn, nyttolast_data) in enumerate(항목들):
        huvud_värde.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SEKUND_värde) for SEKUND_värde in nyttolast_data)))
    huvud_värde.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Namn, nyttolast_data) in enumerate(항목들):
        huvud_värde.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Namn, ensure_ascii=False), 순번, len(nyttolast_data)))
    huvud_värde.append('};')
    (rot_väg / 'build/user/java-resources.h').write_text('\n'.join(huvud_värde) + '\n', encoding='utf-8')
    fördelning_väg = rot_väg / 'dist'; fördelning_väg.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(fördelning_väg / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for relativ_sökväg, _, nyttolast_data in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(relativ_sökväg), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, nyttolast_data)
    with zipfile.ZipFile(str(fördelning_väg / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arkiv:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(rot_väg / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arkiv.writestr(msinfo32_exe, 원본주소.read_bytes())
