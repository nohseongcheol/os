#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/ໂອນອອກ_ໄຟລ໌.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('ໂອນອອກ_ໄຟລ໌', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ໂອນອອກ_ໄຟລ໌')
    대응 = {'data': 'ຂໍ້ມູນ', 'i': '순번', 'name': 'ຊື່', 'c': 'ຈຸດ_ລະ_ຫັດ', 'p': 'ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ', 'args': 'ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
