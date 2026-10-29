#!/usr/bin/env python3
"""명시한 Java umthombo_umthi/iklasi_ixabiso 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ufako_nkcukacha_ixabiso in 항목들:
        if '=' not in ufako_nkcukacha_ixabiso:
            raise ValueError('expected NAME=PATH: ' + ufako_nkcukacha_ixabiso)
        Igama, INDLELA = ufako_nkcukacha_ixabiso.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Igama) or Igama in 명시:
            raise ValueError('invalid or duplicate file name: ' + Igama)
        명시.add(Igama)
        이름들.add(Igama)
        iingcombolo = Path(INDLELA).read_bytes()
        if len(iingcombolo) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Igama)
        파일들.append((Igama.encode('ascii'), iingcombolo))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (Igama, iingcombolo) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, Igama, len(결과), len(iingcombolo))
        결과.extend(iingcombolo)
    return bytes(결과)


if __name__ == '__main__':
    ingcaciso_yegama_ixabiso = argparse.ArgumentParser(description=__doc__)
    ingcaciso_yegama_ixabiso.add_argument('-o', required=True)
    ingcaciso_yegama_ixabiso.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = ingcaciso_yegama_ixabiso.parse_args()
    try:
        iingcombolo = 묶기(인수.files)
        indawo_ekuyiwa_kuyo_ixabiso = Path(인수.o)
        if not indawo_ekuyiwa_kuyo_ixabiso.exists() or indawo_ekuyiwa_kuyo_ixabiso.read_bytes() != iingcombolo:
            임시 = indawo_ekuyiwa_kuyo_ixabiso.with_name(indawo_ekuyiwa_kuyo_ixabiso.name + '.tmp')
            임시.write_bytes(iingcombolo)
            임시.replace(indawo_ekuyiwa_kuyo_ixabiso)
    except (ValueError, OSError) as Impazamo:
        ingcaciso_yegama_ixabiso.error(str(Impazamo))
