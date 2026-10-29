#!/usr/bin/env python3
"""명시한 Java sumber_pepohon/Kelas_VALUE 파일을 permulaan_mesin 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def ikat_peserta(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for pemasukan_VALUE in 항목들:
        if '=' not in pemasukan_VALUE:
            raise ValueError('expected NAME=PATH: ' + pemasukan_VALUE)
        Nama, LALUAN = pemasukan_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Nama) or Nama in 명시:
            raise ValueError('invalid or duplicate file name: ' + Nama)
        명시.add(Nama)
        이름들.add(Nama)
        data = Path(LALUAN).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Nama)
        파일들.append((Nama.encode('ascii'), data))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    ukuran = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    ukuran.extend(bytes(72 * len(파일들)))
    for 수, (Nama, data) in enumerate(파일들):
        struct.pack_into('<64sII', ukuran, 8 + 수 * 72, Nama, len(ukuran), len(data))
        ukuran.extend(data)
    return bytes(ukuran)


if __name__ == '__main__':
    hurai_VALUE = argparse.ArgumentParser(description=__doc__)
    hurai_VALUE.add_argument('-o', required=True)
    hurai_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = hurai_VALUE.parse_args()
    try:
        data = ikat_peserta(인수.files)
        destinasi_VALUE = Path(인수.o)
        if not destinasi_VALUE.exists() or destinasi_VALUE.read_bytes() != data:
            임시 = destinasi_VALUE.with_name(destinasi_VALUE.name + '.tmp')
            임시.write_bytes(data)
            임시.replace(destinasi_VALUE)
    except (ValueError, OSError) as RALAT:
        hurai_VALUE.error(str(RALAT))
