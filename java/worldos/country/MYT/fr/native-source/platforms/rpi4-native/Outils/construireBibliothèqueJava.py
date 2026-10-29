"""interne JVM용 français class/JAR와 EL0에 넣을 lire 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def créerBibliothèqueJava(cheminRacine, exécuterCommande):
    (cheminRacine / 'build/user').mkdir(parents=True, exist_ok=True)
    sortie = cheminRacine / 'build/java-library'
    cheminClasse = sortie / 'classes'
    cheminClasse.mkdir(parents=True, exist_ok=True)
    ListeSources = sorted((cheminRacine / 'JavaFrançais').rglob('*.java'))
    exécuterCommande(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', cheminClasse] + ListeSources)
    listeEntréesListe = []
    for adresseOriginal in ListeSources:
        cheminRelatif = adresseOriginal.relative_to(cheminRacine / 'JavaFrançais').with_suffix('.class')
        donnéesChargeUtile = (cheminClasse / cheminRelatif).read_bytes()
        nom = str(cheminRelatif).replace('/', '.')
        if len(donnéesChargeUtile) > 16384 or len(nom.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + nom)
        listeEntréesListe.append((cheminRelatif, nom, donnéesChargeUtile))
    valeurEntête = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *nom; const unsigned char *Données; unsigned taille; } RessourceClasseJava;']
    for indiceOrdinal, (_, nom, donnéesChargeUtile) in enumerate(listeEntréesListe):
        valeurEntête.append('static const unsigned char donnéesClasseJava%d[] = {%s};' % (indiceOrdinal, ','.join(str(valeurDeuxième) for valeurDeuxième in donnéesChargeUtile)))
    valeurEntête.append('static const RessourceClasseJava listeClasseJava[] = {')
    for indiceOrdinal, (_, nom, donnéesChargeUtile) in enumerate(listeEntréesListe):
        valeurEntête.append('{%s, donnéesClasseJava%d, %d},' % (json.dumps(nom, ensure_ascii=False), indiceOrdinal, len(donnéesChargeUtile)))
    valeurEntête.append('};')
    (cheminRacine / 'build/user/java-resources.h').write_text('\n'.join(valeurEntête) + '\n', encoding='utf-8')
    cheminDistribution = cheminRacine / 'dist'; cheminDistribution.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(cheminDistribution / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as lotJava:
        for cheminRelatif, _, donnéesChargeUtile in listeEntréesListe:
            informationSystème = zipfile.ZipInfo(str(cheminRelatif), date_time=(1980, 1, 1, 0, 0, 0)); informationSystème.compress_type = zipfile.ZIP_DEFLATED
            lotJava.writestr(informationSystème, donnéesChargeUtile)
    with zipfile.ZipFile(str(cheminDistribution / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for adresseOriginal in ListeSources:
            informationSystème = zipfile.ZipInfo(str(adresseOriginal.relative_to(cheminRacine / 'JavaFrançais')), date_time=(1980, 1, 1, 0, 0, 0)); informationSystème.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(informationSystème, adresseOriginal.read_bytes())
