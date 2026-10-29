"""savs JVM용 Latviešu class/JAR와 EL0에 넣을 Lasīt 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(sakne_ceļš, Izpildīt_komanda):
    (sakne_ceļš / 'build/user').mkdir(parents=True, exist_ok=True)
    ražojums = sakne_ceļš / 'build/java-library'
    klase_ceļš = ražojums / 'classes'
    klase_ceļš.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((sakne_ceļš / '한국어자바').rglob('*.java'))
    Izpildīt_komanda(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', klase_ceļš] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        relatīvais_ceļš = 원본주소.relative_to(sakne_ceļš / '한국어자바').with_suffix('.class')
        vērtums_dati = (klase_ceļš / relatīvais_ceļš).read_bytes()
        Nosaukums = str(relatīvais_ceļš).replace('/', '.')
        if len(vērtums_dati) > 16384 or len(Nosaukums.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Nosaukums)
        항목들.append((relatīvais_ceļš, Nosaukums, vērtums_dati))
    galvene_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Nosaukums; const unsigned char *dati; unsigned Izmērs; } 자바자원;']
    for 순번, (_, Nosaukums, vērtums_dati) in enumerate(항목들):
        galvene_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in vērtums_dati)))
    galvene_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Nosaukums, vērtums_dati) in enumerate(항목들):
        galvene_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Nosaukums, ensure_ascii=False), 순번, len(vērtums_dati)))
    galvene_VALUE.append('};')
    (sakne_ceļš / 'build/user/java-resources.h').write_text('\n'.join(galvene_VALUE) + '\n', encoding='utf-8')
    sadale_ceļš = sakne_ceļš / 'dist'; sadale_ceļš.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(sadale_ceļš / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for relatīvais_ceļš, _, vērtums_dati in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(relatīvais_ceļš), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, vērtums_dati)
    with zipfile.ZipFile(str(sadale_ceļš / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arhīvs:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(sakne_ceļš / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arhīvs.writestr(msinfo32_exe, 원본주소.read_bytes())
