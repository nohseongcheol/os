#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/코딩시험.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('코딩시험')
    대응 = {'out': 'ມາດຕະການ_ຂໍ້ມູນ', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'ແລ່ນ', 'elf': '실행파일', 'run': 'ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ', 'name': 'ຊື່', 'path': 'ທາງໂຄຈອນ', 'p': 'ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ', 'ROOT': 'ໂຄງ_ການ_ເລກຮາກ', 'report': 'ໃຊ້ໄດ້_ລາຍງານ', 'args': 'ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
