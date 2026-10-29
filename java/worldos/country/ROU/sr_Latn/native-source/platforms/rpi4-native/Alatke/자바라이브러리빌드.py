"""자체 JVM용 한국어 class/JAR와 EL0에 넣을 읽기 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(koren_putanja, Izvrši_komanda):
    (koren_putanja / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = koren_putanja / 'build/java-library'
    Razred_putanja = 출력결과 / 'classes'
    Razred_putanja.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((koren_putanja / '한국어자바').rglob('*.java'))
    Izvrši_komanda(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Razred_putanja] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        relativna_putanja = 원본주소.relative_to(koren_putanja / '한국어자바').with_suffix('.class')
        korisni_podaci_podaci = (Razred_putanja / relativna_putanja).read_bytes()
        ime = str(relativna_putanja).replace('/', '.')
        if len(korisni_podaci_podaci) > 16384 or len(ime.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + ime)
        항목들.append((relativna_putanja, ime, korisni_podaci_podaci))
    Zaglavlje_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *ime; const unsigned char *podaci; unsigned promeniti_veličinu; } 자바자원;']
    for 순번, (_, ime, korisni_podaci_podaci) in enumerate(항목들):
        Zaglavlje_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in korisni_podaci_podaci)))
    Zaglavlje_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, ime, korisni_podaci_podaci) in enumerate(항목들):
        Zaglavlje_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(ime, ensure_ascii=False), 순번, len(korisni_podaci_podaci)))
    Zaglavlje_VALUE.append('};')
    (koren_putanja / 'build/user/java-resources.h').write_text('\n'.join(Zaglavlje_VALUE) + '\n', encoding='utf-8')
    배포경로 = koren_putanja / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for relativna_putanja, _, korisni_podaci_podaci in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(relativna_putanja), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, korisni_podaci_podaci)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arhiva:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(koren_putanja / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arhiva.writestr(msinfo32_exe, 원본주소.read_bytes())
