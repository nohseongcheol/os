#!/usr/bin/env python3
"""명시한 ຜູ້ໃຊ້ ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    ການແຈກຄໍາສັບ_ຄ່າ = argparse.ArgumentParser()
    ການແຈກຄໍາສັບ_ຄ່າ.add_argument('-o', required=True)
    ການແຈກຄໍາສັບ_ຄ່າ.add_argument('files', nargs='+', help='ຊື່=ELF경로')
    ພາຣາມິເຕີ_ຂໍ້ພິສູດ = ການແຈກຄໍາສັບ_ຄ່າ.parse_args()
    if len(ພາຣາມິເຕີ_ຂໍ້ພິສູດ.files) > 32:
        ການແຈກຄໍາສັບ_ຄ່າ.error('ແອັບ_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ເຂົ້າໃນ_ຄ່າ in ພາຣາມິເຕີ_ຂໍ້ພິສູດ.files:
        ຊື່, ທາງໂຄຈອນ = ເຂົ້າໃນ_ຄ່າ.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', ຊື່) or ຊື່ in 이름들:
            ການແຈກຄໍາສັບ_ຄ່າ.error('ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ 이름이 잘못되었거나 중복됨: ' + ຊື່)
        이름들.add(ຊື່)
        ຂໍ້ມູນ = Path(ທາງໂຄຈອນ).read_bytes()
        if len(ຂໍ້ມູນ) > 2 * 1024 * 1024:
            ການແຈກຄໍາສັບ_ຄ່າ.error('ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ 파일이 너무 큼')
        항목들.append((ຊື່.encode(), ຂໍ້ມູນ))
    ມາດຕະການ = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', ມາດຕະການ, 0, 0x50414b4a, len(항목들))
    for ດັດຊະນີ, (ຊື່, ຂໍ້ມູນ) in enumerate(항목들):
        ມາດຕະການ.extend(bytes((-len(ມາດຕະການ)) % 16))
        struct.pack_into('<16sII', ມາດຕະການ, 8 + ດັດຊະນີ * 24, ຊື່, len(ມາດຕະການ), len(ຂໍ້ມູນ))
        ມາດຕະການ.extend(ຂໍ້ມູນ)
    Path(ພາຣາມິເຕີ_ຂໍ້ພິສູດ.o).write_bytes(ມາດຕະການ)

if __name__ == '__main__':
    묶기()
