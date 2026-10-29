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


class ÜbersetzungsvorgangFehler(Exception):
    pass


class datenLesen:
    def __init__(selbstWert, Daten):
        selbstWert.Daten = Daten
        selbstWert.position = 0

    def lesen(selbstWert, Länge):
        if Länge < 0 or selbstWert.position + Länge > len(selbstWert.Daten):
            raise ÜbersetzungsvorgangFehler('beschnittenWert klasseWert 또는 befehl Daten')
        ergebnis = selbstWert.Daten[selbstWert.position:selbstWert.position + Länge]
        selbstWert.position += Länge
        return ergebnis

    def Zahl(selbstWert, formatWert):
        return struct.unpack('>' + formatWert, selbstWert.lesen(struct.calcsize('>' + formatWert)))[0]


def verändertUTF8Dekodieren(Daten):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    Zeichenkette = Daten.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return Zeichenkette.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class klasseWert:
    def __init__(selbstWert, pfad):
        selbstWert.pfad = pfad
        leserWert = datenLesen(pfad.read_bytes())
        if leserWert.Zahl('I') != 0xcafebabe:
            raise ÜbersetzungsvorgangFehler('Java klasseWert 표식이 아님')
        leserWert.lesen(4)
        elementeintragAnzahl = leserWert.Zahl('H')
        selbstWert.konstanteWert = [None] * elementeintragAnzahl
        Nummer = 1
        while Nummer < elementeintragAnzahl:
            artWert = leserWert.Zahl('B')
            if artWert == 1:
                Wert = verändertUTF8Dekodieren(leserWert.lesen(leserWert.Zahl('H')))
            elif artWert == 3:
                Wert = leserWert.Zahl('i')
            elif artWert == 4:
                Wert = leserWert.lesen(4)
            elif artWert in (5, 6):
                Wert = leserWert.lesen(8)
            elif artWert in (7, 8, 16):
                Wert = leserWert.Zahl('H')
            elif artWert in (9, 10, 11, 12, 18):
                Wert = (leserWert.Zahl('H'), leserWert.Zahl('H'))
            elif artWert == 15:
                Wert = (leserWert.Zahl('B'), leserWert.Zahl('H'))
            else:
                raise ÜbersetzungsvorgangFehler('지원하지 않는 konstanteWert artWert: {}'.format(artWert))
            selbstWert.konstanteWert[Nummer] = (artWert, Wert)
            Nummer += 2 if artWert in (5, 6) else 1
        selbstWert.zugriffEintrag = leserWert.Zahl('H')
        selbstWert.Name = selbstWert.klasseName(leserWert.Zahl('H'))
        elternknotenWert = leserWert.Zahl('H')
        if selbstWert.klasseName(elternknotenWert) != 'java/lang/Object' or leserWert.Zahl('H') != 0:
            raise ÜbersetzungsvorgangFehler(selbstWert.Name + ': 상속 및 인터페이스는 아직 지원하지 않음')
        selbstWert.feldWert = selbstWert.mitgliederLesen(leserWert)
        selbstWert.Funktion = selbstWert.mitgliederLesen(leserWert)
        selbstWert.attributlisteLesen(leserWert)

    def Zeichen(selbstWert, Nummer):
        if selbstWert.konstanteWert[Nummer][0] != 1:
            raise ÜbersetzungsvorgangFehler('Zeichenkette konstanteWert formatWert fehler')
        return selbstWert.konstanteWert[Nummer][1]

    def klasseName(selbstWert, Nummer):
        return selbstWert.Zeichen(selbstWert.konstanteWert[Nummer][1])

    def verweis(selbstWert, Nummer):
        eigentümerWert, nameFormat = selbstWert.konstanteWert[Nummer][1]
        Name, formatWert = selbstWert.konstanteWert[nameFormat][1]
        return selbstWert.klasseName(eigentümerWert), selbstWert.Zeichen(Name), selbstWert.Zeichen(formatWert)

    def attributlisteLesen(selbstWert, leserWert):
        ergebnis = {}
        for _ in range(leserWert.Zahl('H')):
            Name = selbstWert.Zeichen(leserWert.Zahl('H'))
            ergebnis[Name] = leserWert.lesen(leserWert.Zahl('I'))
        return ergebnis

    def mitgliederLesen(selbstWert, leserWert):
        ergebnis = []
        for _ in range(leserWert.Zahl('H')):
            zugriffEintrag = leserWert.Zahl('H')
            Name = selbstWert.Zeichen(leserWert.Zahl('H'))
            formatWert = selbstWert.Zeichen(leserWert.Zahl('H'))
            ergebnis.append((zugriffEintrag, Name, formatWert, selbstWert.attributlisteLesen(leserWert)))
        return ergebnis


def typenAnalysieren(Zeichenkette):
    ergebnis = []
    position = 0
    while position < len(Zeichenkette):
        for formatWert in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if Zeichenkette.startswith(formatWert, position):
                ergebnis.append(formatWert)
                position += len(formatWert)
                break
        else:
            raise ÜbersetzungsvorgangFehler('지원하지 않는 datenTyp: ' + Zeichenkette)
    return ergebnis


def MethodeDeskriptor(beschreibungWert):
    argumente, zurückkehrenErgebnis = beschreibungWert[1:].split(')')
    argumente = typenAnalysieren(argumente)
    zurückkehrenTyp = typenAnalysieren(zurückkehrenErgebnis)
    if 'V' in argumente or len(zurückkehrenTyp) != 1:
        raise ÜbersetzungsvorgangFehler('Funktion beschreibungWert formatWert fehler: ' + beschreibungWert)
    return argumente, zurückkehrenErgebnis


def symbol(artWert, *unterteilWert):
    Quelltext = '\x00'.join(unterteilWert).encode('utf-8')
    return 'j_{}_{}'.format(artWert, hashlib.sha256(Quelltext).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 Funktion 서술에 대해서만 허용한다.
def befehlAusführen(argumente=None):
    Strukturanalysierer = argparse.ArgumentParser(description='eigen Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK quelltextBaum systemErzeugenAbbild')
    Strukturanalysierer.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    Strukturanalysierer.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 eintragAnhängen JAR/klasseWert 디렉터리')
    Strukturanalysierer.add_argument('--java-home', help='openjdk 앱의 systemErzeugenAbbild JDK 또는 openjdk-build의 부트 JDK pfad')
    Strukturanalysierer.add_argument('--bundle-runtime', help='befehlAusführen 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    Strukturanalysierer.add_argument('--cc', default='cc', help='OpenJDK ProgrammStarter/quelltextBaum 빌드의 C Übersetzer')
    Strukturanalysierer.add_argument('--cxx', help='openjdk-build의 C++ Übersetzer')
    Strukturanalysierer.add_argument('--jobs', type=int, default=2, help='openjdk-build의 systemErzeugenAbbild Aufgabe Zahl')
    Strukturanalysierer.add_argument('--openjdk-target', help='공식 OpenJDK 교차 systemErzeugenAbbild zielobjektWert (예: aarch64-linux-gnu)')
    Strukturanalysierer.add_argument('--sysroot', help='교차 systemErzeugenAbbild 대상의 libc/헤더/bibliothek 루트')
    Strukturanalysierer.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 formatWert')
    Strukturanalysierer.add_argument('--export', action='append', default=[], help='외부기호=klasseWert.Funktion (eigen operandStapel ABI)')
    Strukturanalysierer.add_argument('--entry', help='예: berechnung.ausführenVorgang (openjdk-build 이외 대상에서 istErforderlich)')
    Strukturanalysierer.add_argument('-o', '--output', required=True, help='befehlAusführen ELF/.o Ausgabe; openjdk-build는 전용 systemErzeugenAbbild 디렉터리')
    Strukturanalysierer.add_argument('sources', nargs='+')
    parameterArgument = Strukturanalysierer.parse_args(argumente)
    if parameterArgument.target == 'openjdk-build':
        if len(parameterArgument.sources) != 1 or not parameterArgument.java_home or parameterArgument.entry or parameterArgument.export or parameterArgument.classpath or parameterArgument.bundle_runtime:
            raise ÜbersetzungsvorgangFehler('openjdk-build: OpenJDK quelltextBaum 디렉터리 하나와 --java-home 부트 JDK, -o systemErzeugenAbbild 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parameterArgument.sources[0], parameterArgument.output, parameterArgument.java_home, parameterArgument.jobs, parameterArgument.openjdk_target,
                  parameterArgument.sysroot, None if parameterArgument.cc == 'cc' else parameterArgument.cc, parameterArgument.cxx, parameterArgument.configure_arg)
        except BuildError as fehler:
            raise ÜbersetzungsvorgangFehler(str(fehler))
        return
    if not parameterArgument.entry:
        Strukturanalysierer.error('--entry is required for this target')
    if parameterArgument.cxx or parameterArgument.openjdk_target or parameterArgument.sysroot or parameterArgument.configure_arg or parameterArgument.jobs != 2:
        raise ÜbersetzungsvorgangFehler('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build zielobjektWert 전용')
    if parameterArgument.target == 'openjdk':
        sys.modules.setdefault('Übersetzer', sys.modules[__name__])
        from ausführdateiDatei import eintragErstellen
        eintragErstellen(parameterArgument)
        return
    if parameterArgument.classpath or parameterArgument.java_home or parameterArgument.bundle_runtime or parameterArgument.cc != 'cc':
        raise ÜbersetzungsvorgangFehler('classpath/java-home/bundle-runtime/cc 옵션은 openjdk zielobjektWert 전용')
    javaBefehl = ['sh', str(Path(__file__).resolve().parent/'vorabVonElementZeit.sh'),
                '--target', parameterArgument.target, '--entry', parameterArgument.entry, '-o', parameterArgument.output]
    for zuweisenWert in parameterArgument.export: javaBefehl.extend(['--export', zuweisenWert])
    subprocess.run(javaBefehl+parameterArgument.sources, check=True)
    return


if __name__ == '__main__':
    try:
        befehlAusführen()
    except (ÜbersetzungsvorgangFehler, OSError, ValueError, subprocess.CalledProcessError) as fehler:
        print('quelltextÜbersetzen fehler: ' + str(fehler), file=sys.stderr)
        sys.exit(1)
