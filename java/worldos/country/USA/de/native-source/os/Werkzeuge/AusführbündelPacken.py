#!/usr/bin/env python3
"""명시한 Benutzer ELF만 lesen 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def AusführbündelPacken():
    wertAnalysieren = argparse.ArgumentParser()
    wertAnalysieren.add_argument('-o', required=True)
    wertAnalysieren.add_argument('files', nargs='+', help='Name=ELF경로')
    parameterArgument = wertAnalysieren.parse_args()
    if len(parameterArgument.files) > 32:
        wertAnalysieren.error('Programm höchstwertWert 32개')
    einträgeListe = []
    namenListe = set()
    for eintragWert in parameterArgument.files:
        Name, pfad = eintragWert.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Name) or Name in namenListe:
            wertAnalysieren.error('befehlAusführen 이름이 잘못되었거나 중복됨: ' + Name)
        namenListe.add(Name)
        Daten = Path(pfad).read_bytes()
        if len(Daten) > 2 * 1024 * 1024:
            wertAnalysieren.error('befehlAusführen 파일이 너무 큼')
        einträgeListe.append((Name.encode(), Daten))
    ergebnis = bytearray(8 + 24 * len(einträgeListe))
    struct.pack_into('<II', ergebnis, 0, 0x50414b4a, len(einträgeListe))
    for Nummer, (Name, Daten) in enumerate(einträgeListe):
        ergebnis.extend(bytes((-len(ergebnis)) % 16))
        struct.pack_into('<16sII', ergebnis, 8 + Nummer * 24, Name, len(ergebnis), len(Daten))
        ergebnis.extend(Daten)
    Path(parameterArgument.o).write_bytes(ergebnis)

if __name__ == '__main__':
    AusführbündelPacken()
