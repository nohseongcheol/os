#!/usr/bin/env python3
"""제한형 Java의 검증된 javac 바이트코드를 x86 ELF32 네이티브 코드로 변환한다."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import struct
import subprocess
import sys
import tempfile


class ErreurCompilation(Exception):
    pass


class lireDonnées:
    def __init__(valeurSoi, Données):
        valeurSoi.Données = Données
        valeurSoi.position = 0

    def lire(valeurSoi, longueur):
        if longueur < 0 or valeurSoi.position + longueur > len(valeurSoi.Données):
            raise ErreurCompilation('valeurRogné valeurClasse 또는 commande Données')
        résultat = valeurSoi.Données[valeurSoi.position:valeurSoi.position + longueur]
        valeurSoi.position += longueur
        return résultat

    def nombre(valeurSoi, valeurFormat):
        return struct.unpack('>' + valeurFormat, valeurSoi.lire(struct.calcsize('>' + valeurFormat)))[0]


def décoder8UTFModifié(Données):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    Chaîne = Données.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return Chaîne.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class valeurClasse:
    def __init__(valeurSoi, chemin):
        valeurSoi.chemin = chemin
        valeurLecteur = lireDonnées(chemin.read_bytes())
        if valeurLecteur.nombre('I') != 0xcafebabe:
            raise ErreurCompilation('Java valeurClasse 표식이 아님')
        valeurLecteur.lire(4)
        nombreÉlémentsÉlémentListe = valeurLecteur.nombre('H')
        valeurSoi.valeurConstante = [None] * nombreÉlémentsÉlémentListe
        numéro = 1
        while numéro < nombreÉlémentsÉlémentListe:
            valeurGenre = valeurLecteur.nombre('B')
            if valeurGenre == 1:
                valeur = décoder8UTFModifié(valeurLecteur.lire(valeurLecteur.nombre('H')))
            elif valeurGenre == 3:
                valeur = valeurLecteur.nombre('i')
            elif valeurGenre == 4:
                valeur = valeurLecteur.lire(4)
            elif valeurGenre in (5, 6):
                valeur = valeurLecteur.lire(8)
            elif valeurGenre in (7, 8, 16):
                valeur = valeurLecteur.nombre('H')
            elif valeurGenre in (9, 10, 11, 12, 18):
                valeur = (valeurLecteur.nombre('H'), valeurLecteur.nombre('H'))
            elif valeurGenre == 15:
                valeur = (valeurLecteur.nombre('B'), valeurLecteur.nombre('H'))
            else:
                raise ErreurCompilation('지원하지 않는 valeurConstante valeurGenre: {}'.format(valeurGenre))
            valeurSoi.valeurConstante[numéro] = (valeurGenre, valeur)
            numéro += 2 if valeurGenre in (5, 6) else 1
        valeurSoi.entréeÉlémentAccès = valeurLecteur.nombre('H')
        valeurSoi.nom = valeurSoi.nomClasse(valeurLecteur.nombre('H'))
        valeurParent = valeurLecteur.nombre('H')
        if valeurSoi.nomClasse(valeurParent) != 'java/lang/Object' or valeurLecteur.nombre('H') != 0:
            raise ErreurCompilation(valeurSoi.nom + ': 상속 및 인터페이스는 아직 지원하지 않음')
        valeurSoi.valeurChamp = valeurSoi.lireMembres(valeurLecteur)
        valeurSoi.Fonction = valeurSoi.lireMembres(valeurLecteur)
        valeurSoi.lireAttributs(valeurLecteur)

    def Caractères(valeurSoi, numéro):
        if valeurSoi.valeurConstante[numéro][0] != 1:
            raise ErreurCompilation('Chaîne valeurConstante valeurFormat erreur')
        return valeurSoi.valeurConstante[numéro][1]

    def nomClasse(valeurSoi, numéro):
        return valeurSoi.Caractères(valeurSoi.valeurConstante[numéro][1])

    def référence(valeurSoi, numéro):
        valeurPropriétaire, formatNom = valeurSoi.valeurConstante[numéro][1]
        nom, valeurFormat = valeurSoi.valeurConstante[formatNom][1]
        return valeurSoi.nomClasse(valeurPropriétaire), valeurSoi.Caractères(nom), valeurSoi.Caractères(valeurFormat)

    def lireAttributs(valeurSoi, valeurLecteur):
        résultat = {}
        for _ in range(valeurLecteur.nombre('H')):
            nom = valeurSoi.Caractères(valeurLecteur.nombre('H'))
            résultat[nom] = valeurLecteur.lire(valeurLecteur.nombre('I'))
        return résultat

    def lireMembres(valeurSoi, valeurLecteur):
        résultat = []
        for _ in range(valeurLecteur.nombre('H')):
            entréeÉlémentAccès = valeurLecteur.nombre('H')
            nom = valeurSoi.Caractères(valeurLecteur.nombre('H'))
            valeurFormat = valeurSoi.Caractères(valeurLecteur.nombre('H'))
            résultat.append((entréeÉlémentAccès, nom, valeurFormat, valeurSoi.lireAttributs(valeurLecteur)))
        return résultat


def analyserTypes(Chaîne):
    résultat = []
    position = 0
    while position < len(Chaîne):
        for valeurFormat in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if Chaîne.startswith(valeurFormat, position):
                résultat.append(valeurFormat)
                position += len(valeurFormat)
                break
        else:
            raise ErreurCompilation('지원하지 않는 typeDonnées: ' + Chaîne)
    return résultat


def DescripteurMéthode(valeurDescription):
    arguments, résultatRetourner = valeurDescription[1:].split(')')
    arguments = analyserTypes(arguments)
    typeRetourner = analyserTypes(résultatRetourner)
    if 'V' in arguments or len(typeRetourner) != 1:
        raise ErreurCompilation('Fonction valeurDescription valeurFormat erreur: ' + valeurDescription)
    return arguments, résultatRetourner


def symbole(valeurGenre, *valeurSousPartie):
    source = '\x00'.join(valeurSousPartie).encode('utf-8')
    return 'j_{}_{}'.format(valeurGenre, hashlib.sha256(source).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 Fonction 서술에 대해서만 허용한다.
def exécuterCommande(arguments=None):
    Analyseur = argparse.ArgumentParser(description='interne Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK arbreSource construireSystème')
    Analyseur.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    Analyseur.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 ajouterFinEntréeÉlément JAR/valeurClasse 디렉터리')
    Analyseur.add_argument('--java-home', help='openjdk 앱의 construireSystème JDK 또는 openjdk-build의 부트 JDK chemin')
    Analyseur.add_argument('--bundle-runtime', help='exécuterCommande 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    Analyseur.add_argument('--cc', default='cc', help='OpenJDK LanceurProgramme/arbreSource 빌드의 C Compilateur')
    Analyseur.add_argument('--cxx', help='openjdk-build의 C++ Compilateur')
    Analyseur.add_argument('--jobs', type=int, default=2, help='openjdk-build의 construireSystème Tâche nombre')
    Analyseur.add_argument('--openjdk-target', help='공식 OpenJDK 교차 construireSystème valeurCible (예: aarch64-linux-gnu)')
    Analyseur.add_argument('--sysroot', help='교차 construireSystème 대상의 libc/헤더/bibliothèque 루트')
    Analyseur.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 valeurFormat')
    Analyseur.add_argument('--export', action='append', default=[], help='외부기호=valeurClasse.Fonction (interne pileOpérande ABI)')
    Analyseur.add_argument('--entry', help='예: calculRésultat.lancer (openjdk-build 이외 대상에서 estRequis)')
    Analyseur.add_argument('-o', '--output', required=True, help='exécuterCommande ELF/.o Sortie; openjdk-build는 전용 construireSystème 디렉터리')
    Analyseur.add_argument('sources', nargs='+')
    argumentParamètre = Analyseur.parse_args(arguments)
    if argumentParamètre.target == 'openjdk-build':
        if len(argumentParamètre.sources) != 1 or not argumentParamètre.java_home or argumentParamètre.entry or argumentParamètre.export or argumentParamètre.classpath or argumentParamètre.bundle_runtime:
            raise ErreurCompilation('openjdk-build: OpenJDK arbreSource 디렉터리 하나와 --java-home 부트 JDK, -o construireSystème 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(argumentParamètre.sources[0], argumentParamètre.output, argumentParamètre.java_home, argumentParamètre.jobs, argumentParamètre.openjdk_target,
                  argumentParamètre.sysroot, None if argumentParamètre.cc == 'cc' else argumentParamètre.cc, argumentParamètre.cxx, argumentParamètre.configure_arg)
        except BuildError as erreur:
            raise ErreurCompilation(str(erreur))
        return
    if not argumentParamètre.entry:
        Analyseur.error('--entry is required for this target')
    if argumentParamètre.cxx or argumentParamètre.openjdk_target or argumentParamètre.sysroot or argumentParamètre.configure_arg or argumentParamètre.jobs != 2:
        raise ErreurCompilation('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build valeurCible 전용')
    if argumentParamètre.target == 'openjdk':
        sys.modules.setdefault('Compilateur', sys.modules[__name__])
        from fichierCodeExécutable import créerEntréeÉlément
        créerEntréeÉlément(argumentParamètre)
        return
    if argumentParamètre.classpath or argumentParamètre.java_home or argumentParamètre.bundle_runtime or argumentParamètre.cc != 'cc':
        raise ErreurCompilation('classpath/java-home/bundle-runtime/cc 옵션은 openjdk valeurCible 전용')
    commandeJava = ['sh', str(Path(__file__).resolve().parent/'tempsDeAnticipé.sh'),
                '--target', argumentParamètre.target, '--entry', argumentParamètre.entry, '-o', argumentParamètre.output]
    for valeurAffecter in argumentParamètre.export: commandeJava.extend(['--export', valeurAffecter])
    subprocess.run(commandeJava+argumentParamètre.sources, check=True)
    return


if __name__ == '__main__':
    try:
        exécuterCommande()
    except (ErreurCompilation, OSError, ValueError, subprocess.CalledProcessError) as erreur:
        print('compilerSource erreur: ' + str(erreur), file=sys.stderr)
        sys.exit(1)
