#!/usr/bin/env python3
"""명시한 Java ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້/ປະເພດສິ່ງຂອງ_ຄ່າ 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ເຂົ້າໃນ_ຄ່າ in 항목들:
        if '=' not in ເຂົ້າໃນ_ຄ່າ:
            raise ValueError('expected NAME=PATH: ' + ເຂົ້າໃນ_ຄ່າ)
        ຊື່, ທາງໂຄຈອນ = ເຂົ້າໃນ_ຄ່າ.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', ຊື່) or ຊື່ in 명시:
            raise ValueError('invalid or duplicate file name: ' + ຊື່)
        명시.add(ຊື່)
        이름들.add(ຊື່)
        ຂໍ້ມູນ = Path(ທາງໂຄຈອນ).read_bytes()
        if len(ຂໍ້ມູນ) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + ຊື່)
        파일들.append((ຊື່.encode('ascii'), ຂໍ້ມູນ))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    ມາດຕະການ = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    ມາດຕະການ.extend(bytes(72 * len(파일들)))
    for 수, (ຊື່, ຂໍ້ມູນ) in enumerate(파일들):
        struct.pack_into('<64sII', ມາດຕະການ, 8 + 수 * 72, ຊື່, len(ມາດຕະການ), len(ຂໍ້ມູນ))
        ມາດຕະການ.extend(ຂໍ້ມູນ)
    return bytes(ມາດຕະການ)


if __name__ == '__main__':
    ການແຈກຄໍາສັບ_ຄ່າ = argparse.ArgumentParser(description=__doc__)
    ການແຈກຄໍາສັບ_ຄ່າ.add_argument('-o', required=True)
    ການແຈກຄໍາສັບ_ຄ່າ.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = ການແຈກຄໍາສັບ_ຄ່າ.parse_args()
    try:
        ຂໍ້ມູນ = 묶기(인수.files)
        ປາຍທາງ_ຄ່າ = Path(인수.o)
        if not ປາຍທາງ_ຄ່າ.exists() or ປາຍທາງ_ຄ່າ.read_bytes() != ຂໍ້ມູນ:
            임시 = ປາຍທາງ_ຄ່າ.with_name(ປາຍທາງ_ຄ່າ.name + '.tmp')
            임시.write_bytes(ຂໍ້ມູນ)
            임시.replace(ປາຍທາງ_ຄ່າ)
    except (ValueError, OSError) as ຂໍ້ຜິດພາດ:
        ການແຈກຄໍາສັບ_ຄ່າ.error(str(ຂໍ້ຜິດພາດ))
