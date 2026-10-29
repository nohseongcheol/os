"""eigen JVM용 Deutsch class/JAR와 EL0에 넣을 lesen 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def javaBibliothekErstellen(wurzelPfad, befehlAusführen):
    (wurzelPfad / 'build/user').mkdir(parents=True, exist_ok=True)
    ausgabe = wurzelPfad / 'build/java-library'
    klassePfad = ausgabe / 'classes'
    klassePfad.mkdir(parents=True, exist_ok=True)
    Quelltextliste = sorted((wurzelPfad / 'DeutschJava').rglob('*.java'))
    befehlAusführen(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', klassePfad] + Quelltextliste)
    einträgeListe = []
    for ursprünglichAdresse in Quelltextliste:
        relativPfad = ursprünglichAdresse.relative_to(wurzelPfad / 'DeutschJava').with_suffix('.class')
        nutzdatenDaten = (klassePfad / relativPfad).read_bytes()
        Name = str(relativPfad).replace('/', '.')
        if len(nutzdatenDaten) > 16384 or len(Name.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + Name)
        einträgeListe.append((relativPfad, Name, nutzdatenDaten))
    kopfbereichWert = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *Name; const unsigned char *Daten; unsigned größe; } JavaKlasseBetriebsmittelEintrag;']
    for ordnungszahlIndex, (_, Name, nutzdatenDaten) in enumerate(einträgeListe):
        kopfbereichWert.append('static const unsigned char javaKlasseDaten%d[] = {%s};' % (ordnungszahlIndex, ','.join(str(zweiterWert) for zweiterWert in nutzdatenDaten)))
    kopfbereichWert.append('static const JavaKlasseBetriebsmittelEintrag javaKlasseListe[] = {')
    for ordnungszahlIndex, (_, Name, nutzdatenDaten) in enumerate(einträgeListe):
        kopfbereichWert.append('{%s, javaKlasseDaten%d, %d},' % (json.dumps(Name, ensure_ascii=False), ordnungszahlIndex, len(nutzdatenDaten)))
    kopfbereichWert.append('};')
    (wurzelPfad / 'build/user/java-resources.h').write_text('\n'.join(kopfbereichWert) + '\n', encoding='utf-8')
    verteilungPfad = wurzelPfad / 'dist'; verteilungPfad.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(verteilungPfad / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as javaBündel:
        for relativPfad, _, nutzdatenDaten in einträgeListe:
            systemInformation = zipfile.ZipInfo(str(relativPfad), date_time=(1980, 1, 1, 0, 0, 0)); systemInformation.compress_type = zipfile.ZIP_DEFLATED
            javaBündel.writestr(systemInformation, nutzdatenDaten)
    with zipfile.ZipFile(str(verteilungPfad / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as archiv:
        for ursprünglichAdresse in Quelltextliste:
            systemInformation = zipfile.ZipInfo(str(ursprünglichAdresse.relative_to(wurzelPfad / 'DeutschJava')), date_time=(1980, 1, 1, 0, 0, 0)); systemInformation.compress_type = zipfile.ZIP_DEFLATED
            archiv.writestr(systemInformation, ursprünglichAdresse.read_bytes())
