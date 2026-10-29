#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/되돌림시험서버.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'ຂໍ້ມູນ', 'e': '보조항목', 'connection': 'ການເຊື່ອມຕໍ່_e05f319b', 'f': 'ຟາຍ_ເຂົ້າໃນ', 'peer': 'ລຸ້ນດຽວກັນ_ຄ່າ', 'self': '자신', 'udp': '전문제어', 't': 'ເທີມີນໍ_ເຂົ້າໃນ', 'tcp': 'ການເຊື່ອມຕໍ່_ຄວບຄຸມ', 'EchoFixture': '되돌림시험서버', 'args': 'ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
