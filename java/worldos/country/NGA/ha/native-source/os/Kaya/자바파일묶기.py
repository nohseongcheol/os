#!/usr/bin/env python3
"""명시한 Java tushe_Li_irabin_tarin_bayanai/Aji_Daraja 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for Mashigar_bayanai_Daraja in 항목들:
        if '=' not in Mashigar_bayanai_Daraja:
            raise ValueError('expected NAME=PATH: ' + Mashigar_bayanai_Daraja)
        Suna, Hanyar_shiga = Mashigar_bayanai_Daraja.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Suna) or Suna in 명시:
            raise ValueError('invalid or duplicate file name: ' + Suna)
        명시.add(Suna)
        이름들.add(Suna)
        Tarin_bayani = Path(Hanyar_shiga).read_bytes()
        if len(Tarin_bayani) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Suna)
        파일들.append((Suna.encode('ascii'), Tarin_bayani))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (Suna, Tarin_bayani) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, Suna, len(결과), len(Tarin_bayani))
        결과.extend(Tarin_bayani)
    return bytes(결과)


if __name__ == '__main__':
    Daddatse_Daraja = argparse.ArgumentParser(description=__doc__)
    Daddatse_Daraja.add_argument('-o', required=True)
    Daddatse_Daraja.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = Daddatse_Daraja.parse_args()
    try:
        Tarin_bayani = 묶기(인수.files)
        Zangon_ƙarshe_Daraja = Path(인수.o)
        if not Zangon_ƙarshe_Daraja.exists() or Zangon_ƙarshe_Daraja.read_bytes() != Tarin_bayani:
            임시 = Zangon_ƙarshe_Daraja.with_name(Zangon_ƙarshe_Daraja.name + '.tmp')
            임시.write_bytes(Tarin_bayani)
            임시.replace(Zangon_ƙarshe_Daraja)
    except (ValueError, OSError) as Kuskure:
        Daddatse_Daraja.error(str(Kuskure))
