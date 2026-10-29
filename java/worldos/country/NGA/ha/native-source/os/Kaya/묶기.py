#!/usr/bin/env python3
"""명시한 Mai_anfani_da_kwamfuta ELF만 Yi_Karatu 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    Daddatse_Daraja = argparse.ArgumentParser()
    Daddatse_Daraja.add_argument('-o', required=True)
    Daddatse_Daraja.add_argument('files', nargs='+', help='Suna=ELF경로')
    maaunin_Tubalin_aiki = Daddatse_Daraja.parse_args()
    if len(maaunin_Tubalin_aiki.files) > 32:
        Daddatse_Daraja.error('Shiri_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for Mashigar_bayanai_Daraja in maaunin_Tubalin_aiki.files:
        Suna, Hanyar_shiga = Mashigar_bayanai_Daraja.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Suna) or Suna in 이름들:
            Daddatse_Daraja.error('gudanar_Umarni 이름이 잘못되었거나 중복됨: ' + Suna)
        이름들.add(Suna)
        Tarin_bayani = Path(Hanyar_shiga).read_bytes()
        if len(Tarin_bayani) > 2 * 1024 * 1024:
            Daddatse_Daraja.error('gudanar_Umarni 파일이 너무 큼')
        항목들.append((Suna.encode(), Tarin_bayani))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for Indes, (Suna, Tarin_bayani) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + Indes * 24, Suna, len(결과), len(Tarin_bayani))
        결과.extend(Tarin_bayani)
    Path(maaunin_Tubalin_aiki.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()
