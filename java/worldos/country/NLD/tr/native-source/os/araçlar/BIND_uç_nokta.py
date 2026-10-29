#!/usr/bin/env python3
"""명시한 kullanıcı_alanı ELF만 Okuma 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_uç_nokta():
    ayrıştırmak_değer = argparse.ArgumentParser()
    ayrıştırmak_değer.add_argument('-o', required=True)
    ayrıştırmak_değer.add_argument('files', nargs='+', help='İsim=ELF경로')
    parametre_bağımsız_değişken = ayrıştırmak_değer.parse_args()
    if len(parametre_bağımsız_değişken.files) > 32:
        ayrıştırmak_değer.error('program_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for girdi_değer in parametre_bağımsız_değişken.files:
        İsim, yol = girdi_değer.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', İsim) or İsim in 이름들:
            ayrıştırmak_değer.error('yürütmek_komut 이름이 잘못되었거나 중복됨: ' + İsim)
        이름들.add(İsim)
        veri = Path(yol).read_bytes()
        if len(veri) > 2 * 1024 * 1024:
            ayrıştırmak_değer.error('yürütmek_komut 파일이 너무 큼')
        항목들.append((İsim.encode(), veri))
    sonuç = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', sonuç, 0, 0x50414b4a, len(항목들))
    for Dizin, (İsim, veri) in enumerate(항목들):
        sonuç.extend(bytes((-len(sonuç)) % 16))
        struct.pack_into('<16sII', sonuç, 8 + Dizin * 24, İsim, len(sonuç), len(veri))
        sonuç.extend(veri)
    Path(parametre_bağımsız_değişken.o).write_bytes(sonuç)

if __name__ == '__main__':
    BIND_uç_nokta()
