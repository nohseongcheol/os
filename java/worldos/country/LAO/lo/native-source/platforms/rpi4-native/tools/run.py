#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ')
    대응 = {'supported': '지원목록', 'parser': 'ຕົວແຍກວິເຄາະ', 'qemu': '모의기계', 'run_desktop': 'ແລ່ນ_ເດັສທັອບ', 'main': 'ແລ່ນ', 'host': 'ໂຮສ', 'status': 'ສະຖານະ_ຄ່າ', 'NetworkBridge': 'ເຄືອຂ່າຍ_ຕົວເຊື່ອມ', 'ROOT': 'ໂຄງ_ການ_ເລກຮາກ', 'bridge': 'ຕົວເຊື່ອມ', 'loader': '적재기', 'base': 'ພື້ນຫຼັງ_ຄ່າ', 'options': 'ຕົວເລືອກ', 'binary': 'ຖານ_ສອງ', 'args': 'ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ', 'command': 'ຄໍາສັ່ງ_1f12b8e2'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
