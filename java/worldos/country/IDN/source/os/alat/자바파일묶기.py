#!/usr/bin/env python3
"""명시한 Java sumber_pohon/Kelas_VALUE 파일을 awal_mesin 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def ikat_peserta(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for entri_VALUE in 항목들:
        if '=' not in entri_VALUE:
            raise ValueError('expected NAME=PATH: ' + entri_VALUE)
        Nama_2, jalur = entri_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Nama_2) or Nama_2 in 명시:
            raise ValueError('invalid or duplicate file name: ' + Nama_2)
        명시.add(Nama_2)
        이름들.add(Nama_2)
        data = Path(jalur).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Nama_2)
        파일들.append((Nama_2.encode('ascii'), data))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    hasil = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    hasil.extend(bytes(72 * len(파일들)))
    for 수, (Nama_2, data) in enumerate(파일들):
        struct.pack_into('<64sII', hasil, 8 + 수 * 72, Nama_2, len(hasil), len(data))
        hasil.extend(data)
    return bytes(hasil)


if __name__ == '__main__':
    urai_VALUE = argparse.ArgumentParser(description=__doc__)
    urai_VALUE.add_argument('-o', required=True)
    urai_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    argumen = urai_VALUE.parse_args()
    try:
        data = ikat_peserta(argumen.files)
        tujuan_VALUE = Path(argumen.o)
        if not tujuan_VALUE.exists() or tujuan_VALUE.read_bytes() != data:
            임시 = tujuan_VALUE.with_name(tujuan_VALUE.name + '.tmp')
            임시.write_bytes(data)
            임시.replace(tujuan_VALUE)
    except (ValueError, OSError) as galat:
        urai_VALUE.error(str(galat))
