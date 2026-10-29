#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/실행파일시험.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'ມາດຕະການ_ຂໍ້ມູນ', 'expected': '예상결과', 'phoff': 'ແອັບ_ສ່ວນຫົວ_ອອບເຊັດ', 'offset': 'ອອບເຊັດ_ຄ່າ', 'invalid': 'ໃຊ້ບໍ່ໄດ້_ຂໍ້ມູນ', 'path': 'ທາງໂຄຈອນ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'ມາດຕະການ', 'format_': 'ຮູບແບບ_b87fd068', 'main': 'ແລ່ນ', 'content': 'ເນື້ອໃນ_ຄ່າ_cb0f2404', 'source': '원본자료', 'name': 'ຊື່', 'reference': 'ການປຽບທຽບ_ຖານເສັ້ນ', 'ROOT': 'ໂຄງ_ການ_ເລກຮາກ', 'value': 'ຄ່າ', 'report': 'ໃຊ້ໄດ້_ລາຍງານ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
