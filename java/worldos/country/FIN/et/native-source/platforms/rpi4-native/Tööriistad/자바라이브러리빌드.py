"""oma JVM용 Eesti class/JAR와 EL0에 넣을 Lugemine 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(juur_tee, Täida_käsk):
    (juur_tee / 'build/user').mkdir(parents=True, exist_ok=True)
    toodang = juur_tee / 'build/java-library'
    tund_tee = toodang / 'classes'
    tund_tee.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((juur_tee / '한국어자바').rglob('*.java'))
    Täida_käsk(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', tund_tee] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        suhteline_tee = 원본주소.relative_to(juur_tee / '한국어자바').with_suffix('.class')
        last_andmed = (tund_tee / suhteline_tee).read_bytes()
        Nimi_2 = str(suhteline_tee).replace('/', '.')
        if len(last_andmed) > 16384 or len(Nimi_2.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Nimi_2)
        항목들.append((suhteline_tee, Nimi_2, last_andmed))
    Päis_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Nimi_2; const unsigned char *andmed; unsigned Suurus; } 자바자원;']
    for 순번, (_, Nimi_2, last_andmed) in enumerate(항목들):
        Päis_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in last_andmed)))
    Päis_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Nimi_2, last_andmed) in enumerate(항목들):
        Päis_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Nimi_2, ensure_ascii=False), 순번, len(last_andmed)))
    Päis_VALUE.append('};')
    (juur_tee / 'build/user/java-resources.h').write_text('\n'.join(Päis_VALUE) + '\n', encoding='utf-8')
    turustus_tee = juur_tee / 'dist'; turustus_tee.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(turustus_tee / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for suhteline_tee, _, last_andmed in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(suhteline_tee), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, last_andmed)
    with zipfile.ZipFile(str(turustus_tee / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arhiiv:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(juur_tee / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arhiiv.writestr(msinfo32_exe, 원본주소.read_bytes())
