#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/ສ້າງ_ເຄືອຂ່າຍ_243da480.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('ສ້າງ_ເຄືອຂ່າຍ_243da480', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ສ້າງ_ເຄືອຂ່າຍ_243da480')
    대응 = {'obj': 'ຟາຍປາຍທາງ', 'objects': 'ປາຍທາງ_ໄຟລ໌', 'library': 'ຫໍສະຫມຸດ', 'output': '출력결과', 'port': 'ຫມາຍເລກພອດ', 'root': 'ເລກຮາກ_ອີເມວ', 'files': 'ຟາຍ_ລາຍຊື່', 'source': '원본자료', 'run': 'ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ', 'flags': 'ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ', 'path': 'ທາງໂຄຈອນ', 'build_network': 'ສ້າງ_ເຄືອຂ່າຍ_48d29d6d', 'cc': '시언어번역기', 'ar': 'ການສໍາເນົາ_ເຄື່ອງມື'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
