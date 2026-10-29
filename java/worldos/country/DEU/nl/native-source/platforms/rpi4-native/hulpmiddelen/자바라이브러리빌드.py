"""Eigen JVM용 Nederlands class/JAR와 EL0에 넣을 Lezen 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(wortel_pad, Uitvoeren_opdracht):
    (wortel_pad / 'build/user').mkdir(parents=True, exist_ok=True)
    uitvoer = wortel_pad / 'build/java-library'
    les_pad = uitvoer / 'classes'
    les_pad.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((wortel_pad / '한국어자바').rglob('*.java'))
    Uitvoeren_opdracht(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', les_pad] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        relatief_pad = 원본주소.relative_to(wortel_pad / '한국어자바').with_suffix('.class')
        payload_gegevens = (les_pad / relatief_pad).read_bytes()
        Naam = str(relatief_pad).replace('/', '.')
        if len(payload_gegevens) > 16384 or len(Naam.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Naam)
        항목들.append((relatief_pad, Naam, payload_gegevens))
    header_WAARDE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Naam; const unsigned char *gegevens; unsigned Grootte; } 자바자원;']
    for 순번, (_, Naam, payload_gegevens) in enumerate(항목들):
        header_WAARDE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECONDE_WAARDE) for SECONDE_WAARDE in payload_gegevens)))
    header_WAARDE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Naam, payload_gegevens) in enumerate(항목들):
        header_WAARDE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Naam, ensure_ascii=False), 순번, len(payload_gegevens)))
    header_WAARDE.append('};')
    (wortel_pad / 'build/user/java-resources.h').write_text('\n'.join(header_WAARDE) + '\n', encoding='utf-8')
    distributie_pad = wortel_pad / 'dist'; distributie_pad.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(distributie_pad / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for relatief_pad, _, payload_gegevens in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(relatief_pad), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, payload_gegevens)
    with zipfile.ZipFile(str(distributie_pad / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Archief:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(wortel_pad / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Archief.writestr(msinfo32_exe, 원본주소.read_bytes())
