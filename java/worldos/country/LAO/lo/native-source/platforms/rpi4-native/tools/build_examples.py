#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/예제빌드.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'ມາດຕະການ_ຂໍ້ມູນ', 'build_examples': '예제만들기', 'files': 'ຟາຍ_ລາຍຊື່', 'java': '자바실행', 'run': 'ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ', 'path': 'ທາງໂຄຈອນ', 'p': 'ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ', 'readme': 'ຂໍ້ແນະນໍາການໃຊ້', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'ຄົ້ນຫາ_ດັດຊະນີ', 'classes': 'ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ', 'repo': 'ຣີໂພຊິທໍຣີ_ທາງໂຄຈອນ', 'root': 'ເລກຮາກ_ອີເມວ', 'content': 'ເນື້ອໃນ_ຄ່າ_cb0f2404', 'source': '원본자료', 'name': 'ຊື່', 'target': 'ເປົ້າ_ຫມາຍ', 'manifest': '꾸러미명세', 'language': 'ພາ_ສາ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
