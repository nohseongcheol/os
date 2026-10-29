"""eget JVM용 Dansk class/JAR와 EL0에 넣을 Læse 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(rod_sti, Udfør_kommando):
    (rod_sti / 'build/user').mkdir(parents=True, exist_ok=True)
    produktoutput = rod_sti / 'build/java-library'
    Hold_sti = produktoutput / 'classes'
    Hold_sti.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((rod_sti / '한국어자바').rglob('*.java'))
    Udfør_kommando(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Hold_sti] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        relativ_sti = 원본주소.relative_to(rod_sti / '한국어자바').with_suffix('.class')
        nyttedata_data = (Hold_sti / relativ_sti).read_bytes()
        Navn = str(relativ_sti).replace('/', '.')
        if len(nyttedata_data) > 16384 or len(Navn.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Navn)
        항목들.append((relativ_sti, Navn, nyttedata_data))
    Header_VÆRDI = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Navn; const unsigned char *data; unsigned Størrelse; } 자바자원;']
    for 순번, (_, Navn, nyttedata_data) in enumerate(항목들):
        Header_VÆRDI.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SEKUND_VÆRDI) for SEKUND_VÆRDI in nyttedata_data)))
    Header_VÆRDI.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Navn, nyttedata_data) in enumerate(항목들):
        Header_VÆRDI.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Navn, ensure_ascii=False), 순번, len(nyttedata_data)))
    Header_VÆRDI.append('};')
    (rod_sti / 'build/user/java-resources.h').write_text('\n'.join(Header_VÆRDI) + '\n', encoding='utf-8')
    distribution_sti = rod_sti / 'dist'; distribution_sti.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(distribution_sti / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for relativ_sti, _, nyttedata_data in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(relativ_sti), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, nyttedata_data)
    with zipfile.ZipFile(str(distribution_sti / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arkiv:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(rod_sti / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arkiv.writestr(msinfo32_exe, 원본주소.read_bytes())
