#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/셸시험.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'ຈຸດ_ພິ_ກັດ_x', 'msg': 'ເຄືອຂ່າຍ_ອີເມວ', 'i': '순번', 'reply': 'ຕອບກັບ', 'call': '호출', 'args': 'ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ', 'chunk': '조각', 'data': 'ຂໍ້ມູນ', 'proc': 'ຂະ_ບວນ_ການ', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ສົ່ງ', 'file': 'ຟາຍ', 'main': 'ແລ່ນ', 'found': 'ຊອກຫາ_ມາດຕະການ', 'ROOT': 'ໂຄງ_ການ_ເລກຮາກ', 'text': 'ຂໍ້ຄວາມ', 'marker': '확인표시', 'command': 'ຄໍາສັ່ງ_1f12b8e2', 'expected': '예상결과', 'pixel': 'ເປ_ລ', 'shell': 'ເຊລ', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'ຈົບ_ອອບເຊັດ', 'image': 'ຮູບ', 'key': '누름값', 'y': 'ປຸ່ມ_Y_ຈຸດປະສານ', 'output': '출력결과', 'result': 'ມາດຕະການ', 'client': 'ລູກຂ່າຍ', 'line': 'ສາຍ', 'stream': 'ສະຕຣີມ_ຄ່າ', 'name': 'ຊື່', 'value': 'ຄ່າ', 'receive': '수신하기', 'report': 'ໃຊ້ໄດ້_ລາຍງານ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
