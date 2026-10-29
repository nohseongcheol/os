#!/usr/bin/env python3
"""명시한 gebruikersruimte ELF만 Lezen 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_eindpunt():
    parseren_WAARDE = argparse.ArgumentParser()
    parseren_WAARDE.add_argument('-o', required=True)
    parseren_WAARDE.add_argument('files', nargs='+', help='Naam=ELF경로')
    parameter_argument = parseren_WAARDE.parse_args()
    if len(parameter_argument.files) > 32:
        parseren_WAARDE.error('app_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for invoer_WAARDE_962f286b in parameter_argument.files:
        Naam, pad = invoer_WAARDE_962f286b.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Naam) or Naam in 이름들:
            parseren_WAARDE.error('Uitvoeren_opdracht 이름이 잘못되었거나 중복됨: ' + Naam)
        이름들.add(Naam)
        gegevens = Path(pad).read_bytes()
        if len(gegevens) > 2 * 1024 * 1024:
            parseren_WAARDE.error('Uitvoeren_opdracht 파일이 너무 큼')
        항목들.append((Naam.encode(), gegevens))
    resultaat = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', resultaat, 0, 0x50414b4a, len(항목들))
    for INDEX, (Naam, gegevens) in enumerate(항목들):
        resultaat.extend(bytes((-len(resultaat)) % 16))
        struct.pack_into('<16sII', resultaat, 8 + INDEX * 24, Naam, len(resultaat), len(gegevens))
        resultaat.extend(gegevens)
    Path(parameter_argument.o).write_bytes(resultaat)

if __name__ == '__main__':
    BIND_eindpunt()
