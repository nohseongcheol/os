"""vlastiti JVM용 hrvatski class/JAR와 EL0에 넣을 Čitaj 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(korijen_put, Izvrši_naredba):
    (korijen_put / 'build/user').mkdir(parents=True, exist_ok=True)
    출력결과 = korijen_put / 'build/java-library'
    poduka_put = 출력결과 / 'classes'
    poduka_put.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((korijen_put / '한국어자바').rglob('*.java'))
    Izvrši_naredba(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', poduka_put] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        relativni_put = 원본주소.relative_to(korijen_put / '한국어자바').with_suffix('.class')
        korisni_podaci_podaci = (poduka_put / relativni_put).read_bytes()
        Ime = str(relativni_put).replace('/', '.')
        if len(korisni_podaci_podaci) > 16384 or len(Ime.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Ime)
        항목들.append((relativni_put, Ime, korisni_podaci_podaci))
    Zaglavlje_VALUE = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Ime; const unsigned char *podaci; unsigned Veličina; } 자바자원;']
    for 순번, (_, Ime, korisni_podaci_podaci) in enumerate(항목들):
        Zaglavlje_VALUE.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SECOND_VALUE) for SECOND_VALUE in korisni_podaci_podaci)))
    Zaglavlje_VALUE.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Ime, korisni_podaci_podaci) in enumerate(항목들):
        Zaglavlje_VALUE.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Ime, ensure_ascii=False), 순번, len(korisni_podaci_podaci)))
    Zaglavlje_VALUE.append('};')
    (korijen_put / 'build/user/java-resources.h').write_text('\n'.join(Zaglavlje_VALUE) + '\n', encoding='utf-8')
    배포경로 = korijen_put / 'dist'; 배포경로.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for relativni_put, _, korisni_podaci_podaci in 항목들:
            Podaci_o_sustavu = zipfile.ZipInfo(str(relativni_put), date_time=(1980, 1, 1, 0, 0, 0)); Podaci_o_sustavu.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(Podaci_o_sustavu, korisni_podaci_podaci)
    with zipfile.ZipFile(str(배포경로 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arhiva:
        for 원본주소 in 원문목록:
            Podaci_o_sustavu = zipfile.ZipInfo(str(원본주소.relative_to(korijen_put / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); Podaci_o_sustavu.compress_type = zipfile.ZIP_DEFLATED
            Arhiva.writestr(Podaci_o_sustavu, 원본주소.read_bytes())
