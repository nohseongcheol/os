"""własny JVM용 polski class/JAR와 EL0에 넣을 Odczyt 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(korzeń_ścieżka, Wykonaj_polecenie):
    (korzeń_ścieżka / 'build/user').mkdir(parents=True, exist_ok=True)
    produkt_wyjściowy = korzeń_ścieżka / 'build/java-library'
    Klasa_ścieżka = produkt_wyjściowy / 'classes'
    Klasa_ścieżka.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((korzeń_ścieżka / '한국어자바').rglob('*.java'))
    Wykonaj_polecenie(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Klasa_ścieżka] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        ścieżka_względna = 원본주소.relative_to(korzeń_ścieżka / '한국어자바').with_suffix('.class')
        ładunek_dane = (Klasa_ścieżka / ścieżka_względna).read_bytes()
        Nazwa = str(ścieżka_względna).replace('/', '.')
        if len(ładunek_dane) > 16384 or len(Nazwa.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Nazwa)
        항목들.append((ścieżka_względna, Nazwa, ładunek_dane))
    Nagłówek_WARTOŚĆ = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Nazwa; const unsigned char *dane; unsigned Rozmiar; } 자바자원;']
    for 순번, (_, Nazwa, ładunek_dane) in enumerate(항목들):
        Nagłówek_WARTOŚĆ.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SEKUNDA_WARTOŚĆ) for SEKUNDA_WARTOŚĆ in ładunek_dane)))
    Nagłówek_WARTOŚĆ.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Nazwa, ładunek_dane) in enumerate(항목들):
        Nagłówek_WARTOŚĆ.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Nazwa, ensure_ascii=False), 순번, len(ładunek_dane)))
    Nagłówek_WARTOŚĆ.append('};')
    (korzeń_ścieżka / 'build/user/java-resources.h').write_text('\n'.join(Nagłówek_WARTOŚĆ) + '\n', encoding='utf-8')
    dystrybucja_ścieżka = korzeń_ścieżka / 'dist'; dystrybucja_ścieżka.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(dystrybucja_ścieżka / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for ścieżka_względna, _, ładunek_dane in 항목들:
            msinfo32_exe = zipfile.ZipInfo(str(ścieżka_względna), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(msinfo32_exe, ładunek_dane)
    with zipfile.ZipFile(str(dystrybucja_ścieżka / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Archiwum:
        for 원본주소 in 원문목록:
            msinfo32_exe = zipfile.ZipInfo(str(원본주소.relative_to(korzeń_ścieżka / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); msinfo32_exe.compress_type = zipfile.ZIP_DEFLATED
            Archiwum.writestr(msinfo32_exe, 원본주소.read_bytes())
