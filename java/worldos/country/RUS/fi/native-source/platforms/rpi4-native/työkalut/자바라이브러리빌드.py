"""oma JVM용 suomi class/JAR와 EL0에 넣을 Luku 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(juuri_polku, Suorita_komento):
    (juuri_polku / 'build/user').mkdir(parents=True, exist_ok=True)
    tulos = juuri_polku / 'build/java-library'
    Luokka_polku = tulos / 'classes'
    Luokka_polku.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((juuri_polku / '한국어자바').rglob('*.java'))
    Suorita_komento(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Luokka_polku] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        suhteellinen_polku = 원본주소.relative_to(juuri_polku / '한국어자바').with_suffix('.class')
        tiedot_data = (Luokka_polku / suhteellinen_polku).read_bytes()
        Nimi = str(suhteellinen_polku).replace('/', '.')
        if len(tiedot_data) > 16384 or len(Nimi.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Nimi)
        항목들.append((suhteellinen_polku, Nimi, tiedot_data))
    otsikko_ARVO = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Nimi; const unsigned char *data; unsigned Koko; } 자바자원;']
    for 순번, (_, Nimi, tiedot_data) in enumerate(항목들):
        otsikko_ARVO.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SEKUNNIT_ARVO) for SEKUNNIT_ARVO in tiedot_data)))
    otsikko_ARVO.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Nimi, tiedot_data) in enumerate(항목들):
        otsikko_ARVO.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Nimi, ensure_ascii=False), 순번, len(tiedot_data)))
    otsikko_ARVO.append('};')
    (juuri_polku / 'build/user/java-resources.h').write_text('\n'.join(otsikko_ARVO) + '\n', encoding='utf-8')
    jakelu_polku = juuri_polku / 'dist'; jakelu_polku.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(jakelu_polku / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for suhteellinen_polku, _, tiedot_data in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(suhteellinen_polku), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, tiedot_data)
    with zipfile.ZipFile(str(jakelu_polku / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Arkisto:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(juuri_polku / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Arkisto.writestr(msinfo32_exe, 원본주소.read_bytes())
