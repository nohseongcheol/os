#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'ມາດຕະການ_ຂໍ້ມູນ', 'builtins': '내장연산', 'header': 'ສ່ວນຫົວ_ຄ່າ', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ', 'flags': 'ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ', 'path': 'ທາງໂຄຈອນ', 'p': 'ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ', 'cc': '시언어번역기', 'obj': 'ຟາຍປາຍທາງ', 'flag': 'ການຕັ້ງຄ່າ_ຄ່າ', 'ld': '연결편집기', 'objects': 'ປາຍທາງ_ໄຟລ໌', 'repo': 'ຣີໂພຊິທໍຣີ_ທາງໂຄຈອນ', 'v': '임시값', 'upstream': 'ຕົ້ນນ້ໍາ', 'root': 'ເລກຮາກ_ອີເມວ', 'assets': '탑재자료', 'source': '원본자료', 'name': 'ຊື່', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
