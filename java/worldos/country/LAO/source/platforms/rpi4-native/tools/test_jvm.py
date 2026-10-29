#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/자바가상기계시험.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'ສະຕຣິງ_ຂໍ້ມູນ', 'actual': 'ຕົວ_ຈິງ_ມາດຕະການ', 'match': '일치', 'payload': 'ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'ແລ່ນ', 'ROOT': 'ໂຄງ_ການ_ເລກຮາກ', 'text': 'ຂໍ້ຄວາມ', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ', 'output': '출력결과', 'result': 'ມາດຕະການ', 'cmd': '명령인수', 'name': 'ຊື່', 'jar': '자바꾸러미', 'report': 'ໃຊ້ໄດ້_ລາຍງານ', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
