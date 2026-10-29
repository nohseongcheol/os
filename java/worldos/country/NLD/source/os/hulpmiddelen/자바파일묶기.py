#!/usr/bin/env python3
"""명시한 Java bron_structuur/les_WAARDE 파일을 machineopstart 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_eindpunt(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for invoer_WAARDE_962f286b in 항목들:
        if '=' not in invoer_WAARDE_962f286b:
            raise ValueError('expected NAME=PATH: ' + invoer_WAARDE_962f286b)
        Naam, pad = invoer_WAARDE_962f286b.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Naam) or Naam in 명시:
            raise ValueError('invalid or duplicate file name: ' + Naam)
        명시.add(Naam)
        이름들.add(Naam)
        gegevens = Path(pad).read_bytes()
        if len(gegevens) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Naam)
        파일들.append((Naam.encode('ascii'), gegevens))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    resultaat = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    resultaat.extend(bytes(72 * len(파일들)))
    for nummer, (Naam, gegevens) in enumerate(파일들):
        struct.pack_into('<64sII', resultaat, 8 + nummer * 72, Naam, len(resultaat), len(gegevens))
        resultaat.extend(gegevens)
    return bytes(resultaat)


if __name__ == '__main__':
    parseren_WAARDE = argparse.ArgumentParser(description=__doc__)
    parseren_WAARDE.add_argument('-o', required=True)
    parseren_WAARDE.add_argument('files', nargs='*', help='NAME=PATH')
    argumenten = parseren_WAARDE.parse_args()
    try:
        gegevens = BIND_eindpunt(argumenten.files)
        doel_WAARDE = Path(argumenten.o)
        if not doel_WAARDE.exists() or doel_WAARDE.read_bytes() != gegevens:
            임시 = doel_WAARDE.with_name(doel_WAARDE.name + '.tmp')
            임시.write_bytes(gegevens)
            임시.replace(doel_WAARDE)
    except (ValueError, OSError) as fout:
        parseren_WAARDE.error(str(fout))
