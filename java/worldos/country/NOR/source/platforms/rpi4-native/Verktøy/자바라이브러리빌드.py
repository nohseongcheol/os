"""eget JVM용 norsk class/JAR와 EL0에 넣을 Les 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(rot_bane, Utfør_kommando):
    (rot_bane / 'build/user').mkdir(parents=True, exist_ok=True)
    produksjon = rot_bane / 'build/java-library'
    time_bane = produksjon / 'classes'
    time_bane.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((rot_bane / '한국어자바').rglob('*.java'))
    Utfør_kommando(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', time_bane] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        relativ_bane = 원본주소.relative_to(rot_bane / '한국어자바').with_suffix('.class')
        nyttelast_data = (time_bane / relativ_bane).read_bytes()
        Navn = str(relativ_bane).replace('/', '.')
        if len(nyttelast_data) > 16384 or len(Navn.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Navn)
        항목들.append((relativ_bane, Navn, nyttelast_data))
    Topptekst_VERDI = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Navn; const unsigned char *data; unsigned Størrelse; } 자바자원;']
    for 순번, (_, Navn, nyttelast_data) in enumerate(항목들):
        Topptekst_VERDI.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SEKUND_VERDI) for SEKUND_VERDI in nyttelast_data)))
    Topptekst_VERDI.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Navn, nyttelast_data) in enumerate(항목들):
        Topptekst_VERDI.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Navn, ensure_ascii=False), 순번, len(nyttelast_data)))
    Topptekst_VERDI.append('};')
    (rot_bane / 'build/user/java-resources.h').write_text('\n'.join(Topptekst_VERDI) + '\n', encoding='utf-8')
    distribusjon_bane = rot_bane / 'dist'; distribusjon_bane.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(distribusjon_bane / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for relativ_bane, _, nyttelast_data in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(relativ_bane), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, nyttelast_data)
    with zipfile.ZipFile(str(distribusjon_bane / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arkiv:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(rot_bane / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arkiv.writestr(msinfo32_exe, 원본주소.read_bytes())
