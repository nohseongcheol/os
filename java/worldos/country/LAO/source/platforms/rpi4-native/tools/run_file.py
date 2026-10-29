#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຟາຍ.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('ປະ_ຕິ_ບັດ_ຟາຍ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ປະ_ຕິ_ບັດ_ຟາຍ')
    대응 = {'timeout': '시간제한', 's': 'ສະຕຣິງ_ຂໍ້ມູນ', 'i': '순번', 'match': '일치', 'files': 'ຟາຍ_ລາຍຊື່', 'program': 'ແອັບ', 'executable': '실행가능파일', 'args': 'ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ', 'chunk': '조각', 'data': 'ຂໍ້ມູນ', 'proc': 'ຂະ_ບວນ_ການ', 'send': 'ສົ່ງ', 'main': 'ແລ່ນ', 'marker': '확인표시', 'command': 'ຄໍາສັ່ງ_1f12b8e2', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ', 'p': 'ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ', 'parser': 'ຕົວແຍກວິເຄາະ', 'options': 'ຕົວເລືອກ', 'kind': 'ຫມວດ_ຄ່າ', 'selector': 'ຕົວ_ໃຊ້_ເລືອກ', 'upload_data': 'ໂອນອອກ_ຂໍ້ມູນ', 'end': 'ຈົບ_ອອບເຊັດ', 'n': '개수', 'd': 'ປາຍທາງ_ຂໍ້ມູນ', 'key': '누름값', 'output': '출력결과', 'line': 'ສາຍ', 'name': 'ຊື່', 'upload_name': 'ໂອນອອກ_ຊື່', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
