"""vlastní JVM용 čeština class/JAR와 EL0에 넣을 Čtení 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 자바라이브러리만들기(kořen_cesta, Provést_příkaz):
    (kořen_cesta / 'build/user').mkdir(parents=True, exist_ok=True)
    výstup = kořen_cesta / 'build/java-library'
    Třída_cesta = výstup / 'classes'
    Třída_cesta.mkdir(parents=True, exist_ok=True)
    원문목록 = sorted((kořen_cesta / '한국어자바').rglob('*.java'))
    Provést_příkaz(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', Třída_cesta] + 원문목록)
    항목들 = []
    for 원본주소 in 원문목록:
        relativní_cesta = 원본주소.relative_to(kořen_cesta / '한국어자바').with_suffix('.class')
        vytížení_data = (Třída_cesta / relativní_cesta).read_bytes()
        Název = str(relativní_cesta).replace('/', '.')
        if len(vytížení_data) > 16384 or len(Název.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Název)
        항목들.append((relativní_cesta, Název, vytížení_data))
    Nadpis_HODNOTA = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Název; const unsigned char *data; unsigned Velikost; } 자바자원;']
    for 순번, (_, Název, vytížení_data) in enumerate(항목들):
        Nadpis_HODNOTA.append('static const unsigned char 자바클래스자료_%d[] = {%s};' % (순번, ','.join(str(SEKUNDA_HODNOTA) for SEKUNDA_HODNOTA in vytížení_data)))
    Nadpis_HODNOTA.append('static const 자바자원 자바클래스들[] = {')
    for 순번, (_, Název, vytížení_data) in enumerate(항목들):
        Nadpis_HODNOTA.append('{%s, 자바클래스자료_%d, %d},' % (json.dumps(Název, ensure_ascii=False), 순번, len(vytížení_data)))
    Nadpis_HODNOTA.append('};')
    (kořen_cesta / 'build/user/java-resources.h').write_text('\n'.join(Nadpis_HODNOTA) + '\n', encoding='utf-8')
    distribuce_cesta = kořen_cesta / 'dist'; distribuce_cesta.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(distribuce_cesta / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as 자바꾸러미:
        for relativní_cesta, _, vytížení_data in 항목들:
            Informace_o_systému = zipfile.ZipInfo(str(relativní_cesta), date_time=(1980, 1, 1, 0, 0, 0)); Informace_o_systému.compress_type = zipfile.ZIP_DEFLATED
            자바꾸러미.writestr(Informace_o_systému, vytížení_data)
    with zipfile.ZipFile(str(distribuce_cesta / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as Archiv:
        for 원본주소 in 원문목록:
            Informace_o_systému = zipfile.ZipInfo(str(원본주소.relative_to(kořen_cesta / '한국어자바')), date_time=(1980, 1, 1, 0, 0, 0)); Informace_o_systému.compress_type = zipfile.ZIP_DEFLATED
            Archiv.writestr(Informace_o_systému, 원본주소.read_bytes())
