#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/개발꾸러미내보내기.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('개발꾸러미내보내기')
    대응 = {'out': 'ມາດຕະການ_ຂໍ້ມູນ', 'obj': 'ຟາຍປາຍທາງ', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'ການສໍາເນົາ', 'main': 'ແລ່ນ', 'posix': '포직스경로', 'files': 'ຟາຍ_ລາຍຊື່', 'source': '원본자료', 'name': 'ຊື່', 'target': 'ເປົ້າ_ຫມາຍ', 'ROOT': 'ໂຄງ_ການ_ເລກຮາກ', 'destination': 'ປາຍທາງ_ຂໍ້ມູນ_ອີເມວ', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
