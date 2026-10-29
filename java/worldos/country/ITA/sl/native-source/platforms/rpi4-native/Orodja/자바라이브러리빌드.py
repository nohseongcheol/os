"""lastno JVM용 slovenščina class/JAR와 EL0에 넣을 Branje 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(koren_pot, Izvedi_ukaz):
    (koren_pot / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = koren_pot / 'build/java-library'
    Razred_pot = 출력결과 / 'classes'
    Razred_pot.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((koren_pot / '한국어자바').rglob('*.java'))
    Izvedi_ukaz(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Razred_pot] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        relativna_pot = 원본주소.relative_to(koren_pot / '한국어자바').with_suffix('.class')
        koristna_vsebina_podatki = (Razred_pot / relativna_pot).read_bytes()
        Ime = str(relativna_pot).replace('/', '.')
        if len(koristna_vsebina_podatki) > 16384 or len(Ime.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Ime)
        항목들.append((relativna_pot, Ime, koristna_vsebina_podatki))
    Glava_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Ime; const unsigned char *podatki; unsigned Velikost; } 자바자원;']
    for 순번, (_, Ime, koristna_vsebina_podatki) in enumerate(항목들):
        Glava_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in koristna_vsebina_podatki)))
    Glava_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Ime, koristna_vsebina_podatki) in enumerate(항목들):
        Glava_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Ime, ensure_ascii=False), 순번, len(koristna_vsebina_podatki)))
    Glava_VALUE.append('};')
    (koren_pot / 'build/user/java-resources.h').write_text('\n'.join(Glava_VALUE) + '\n', encoding='utf-8')
    배포경로 = koren_pot / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for relativna_pot, _, koristna_vsebina_podatki in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(relativna_pot), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, koristna_vsebina_podatki)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arhiv:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(koren_pot / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arhiv.writestr(msinfo32_exe, 원본주소.read_bytes())
