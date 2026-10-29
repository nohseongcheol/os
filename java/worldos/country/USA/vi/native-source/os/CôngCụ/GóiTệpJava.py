#!/usr/bin/env python3
"""명시한 Java câyNguồn/giáTrịLớp 파일을 KhởiĐộng 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def GóiTệpThựcThi(danhSáchCácMục):
    cácMụcTệp = []
    danhSáchCácTên = {'Hello.java'}
    cácTênTườngMinh = set()
    for giáTrịMục in danhSáchCácMục:
        if '=' not in giáTrịMục:
            raise ValueError('expected NAME=PATH: ' + giáTrịMục)
        tên, đườngDẫn = giáTrịMục.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', tên) or tên in cácTênTườngMinh:
            raise ValueError('invalid or duplicate file name: ' + tên)
        cácTênTườngMinh.add(tên)
        danhSáchCácTên.add(tên)
        DữLiệu = Path(đườngDẫn).read_bytes()
        if len(DữLiệu) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + tên)
        cácMụcTệp.append((tên.encode('ascii'), DữLiệu))
    if len(danhSáchCácTên) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    kếtQuả = bytearray(struct.pack('<4sI', b'JKJF', len(cácMụcTệp)))
    kếtQuả.extend(bytes(72 * len(cácMụcTệp)))
    for trịSố, (tên, DữLiệu) in enumerate(cácMụcTệp):
        struct.pack_into('<64sII', kếtQuả, 8 + trịSố * 72, tên, len(kếtQuả), len(DữLiệu))
        kếtQuả.extend(DữLiệu)
    return bytes(kếtQuả)


if __name__ == '__main__':
    phânTíchCúPhápGiáTrị = argparse.ArgumentParser(description=__doc__)
    phânTíchCúPhápGiáTrị.add_argument('-o', required=True)
    phânTíchCúPhápGiáTrị.add_argument('files', nargs='*', help='NAME=PATH')
    cácĐốiSố = phânTíchCúPhápGiáTrị.parse_args()
    try:
        DữLiệu = GóiTệpThựcThi(cácĐốiSố.files)
        giáTrịĐích = Path(cácĐốiSố.o)
        if not giáTrịĐích.exists() or giáTrịĐích.read_bytes() != DữLiệu:
            giáTrịTạm = giáTrịĐích.with_name(giáTrịĐích.name + '.tmp')
            giáTrịTạm.write_bytes(DữLiệu)
            giáTrịTạm.replace(giáTrịĐích)
    except (ValueError, OSError) as lỗi:
        phânTíchCúPhápGiáTrị.error(str(lỗi))
