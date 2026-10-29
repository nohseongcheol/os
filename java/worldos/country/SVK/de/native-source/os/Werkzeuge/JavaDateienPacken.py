#!/usr/bin/env python3
"""명시한 Java quelltextBaum/klasseWert 파일을 Startvorgang 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def AusführbündelPacken(einträgeListe):
    dateiEinträge = []
    namenListe = {'Hello.java'}
    ausdrücklichNamen = set()
    for eintragWert in einträgeListe:
        if '=' not in eintragWert:
            raise ValueError('expected NAME=PATH: ' + eintragWert)
        Name, pfad = eintragWert.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Name) or Name in ausdrücklichNamen:
            raise ValueError('invalid or duplicate file name: ' + Name)
        ausdrücklichNamen.add(Name)
        namenListe.add(Name)
        Daten = Path(pfad).read_bytes()
        if len(Daten) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Name)
        dateiEinträge.append((Name.encode('ascii'), Daten))
    if len(namenListe) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    ergebnis = bytearray(struct.pack('<4sI', b'JKJF', len(dateiEinträge)))
    ergebnis.extend(bytes(72 * len(dateiEinträge)))
    for Zahl, (Name, Daten) in enumerate(dateiEinträge):
        struct.pack_into('<64sII', ergebnis, 8 + Zahl * 72, Name, len(ergebnis), len(Daten))
        ergebnis.extend(Daten)
    return bytes(ergebnis)


if __name__ == '__main__':
    wertAnalysieren = argparse.ArgumentParser(description=__doc__)
    wertAnalysieren.add_argument('-o', required=True)
    wertAnalysieren.add_argument('files', nargs='*', help='NAME=PATH')
    argumente = wertAnalysieren.parse_args()
    try:
        Daten = AusführbündelPacken(argumente.files)
        zielWert = Path(argumente.o)
        if not zielWert.exists() or zielWert.read_bytes() != Daten:
            vorläufigWert = zielWert.with_name(zielWert.name + '.tmp')
            vorläufigWert.write_bytes(Daten)
            vorläufigWert.replace(zielWert)
    except (ValueError, OSError) as fehler:
        wertAnalysieren.error(str(fehler))
