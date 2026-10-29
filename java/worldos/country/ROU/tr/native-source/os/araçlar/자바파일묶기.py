#!/usr/bin/env python3
"""명시한 Java kaynak_ağaç/Sınıf_değer 파일을 makine_başlatma 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_uç_nokta(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for girdi_değer in 항목들:
        if '=' not in girdi_değer:
            raise ValueError('expected NAME=PATH: ' + girdi_değer)
        İsim, yol = girdi_değer.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', İsim) or İsim in 명시:
            raise ValueError('invalid or duplicate file name: ' + İsim)
        명시.add(İsim)
        이름들.add(İsim)
        veri = Path(yol).read_bytes()
        if len(veri) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + İsim)
        파일들.append((İsim.encode('ascii'), veri))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    sonuç = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    sonuç.extend(bytes(72 * len(파일들)))
    for 수, (İsim, veri) in enumerate(파일들):
        struct.pack_into('<64sII', sonuç, 8 + 수 * 72, İsim, len(sonuç), len(veri))
        sonuç.extend(veri)
    return bytes(sonuç)


if __name__ == '__main__':
    ayrıştırmak_değer = argparse.ArgumentParser(description=__doc__)
    ayrıştırmak_değer.add_argument('-o', required=True)
    ayrıştırmak_değer.add_argument('files', nargs='*', help='NAME=PATH')
    bağımsız_değişkenler = ayrıştırmak_değer.parse_args()
    try:
        veri = BIND_uç_nokta(bağımsız_değişkenler.files)
        hedef_değer = Path(bağımsız_değişkenler.o)
        if not hedef_değer.exists() or hedef_değer.read_bytes() != veri:
            임시 = hedef_değer.with_name(hedef_değer.name + '.tmp')
            임시.write_bytes(veri)
            임시.replace(hedef_değer)
    except (ValueError, OSError) as hata:
        ayrıştırmak_değer.error(str(hata))
