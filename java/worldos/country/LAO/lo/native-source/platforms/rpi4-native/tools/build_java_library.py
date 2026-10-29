#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'ສ່ວນຫົວ_ຄ່າ', 'sources': '원문목록', 'i': '순번', 'info': 'ລະບົບ_ຂໍ້_ມູນ', 'payload': 'ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ', 'src': '원본주소', 'run': 'ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ', 'dist': '배포경로', 'archive': 'ການສໍາເນົາ', 'output': '출력결과', 'root': 'ເລກຮາກ_ອີເມວ', 'name': 'ຊື່', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
