#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/바탕화면시험.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'ຈຸດ_ພິ_ກັດ_x', 'typing': '글자입력', 'message': '알림문', 'start': 'ແລ່ນ', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'ສັນຍາລັກ', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'ຂະ_ບວນ_ການ', 'data': 'ຂໍ້ມູນ', 'main': 'ແລ່ນ', 'w': '너비값', 'init': '초기값', 'block': 'ຂໍ້ມູນ_ບລັອກ', 'ROOT': 'ໂຄງ_ການ_ເລກຮາກ', 'text': 'ຂໍ້ຄວາມ', 'marker': '확인표시', 'report': 'ໃຊ້ໄດ້_ລາຍງານ', 'until': '까지', 'clipboard': 'ຄລິບບອດ_ຄ່າ', 'dst': 'ປາຍທາງ_ອີເມວ', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'ຫມາຍເລກພອດ', 'offset': 'ອອບເຊັດ_ຄ່າ', 'h': '높이값', 'src': '원본주소', 'event': 'ງານ', 'encoding': 'ຊຸດ_ຕົວ_ອັກ_ສອນ', 'size': 'ຂະ_ຫນາດ', 'key': '누름값', 'pixels': '화소들', 'y': 'ປຸ່ມ_Y_ຈຸດປະສານ', 'output': '출력결과', 'symbol': 'ສັນຍາລັກ_ຄ່າ', 'client': 'ລູກຂ່າຍ', 'char': 'ຕົວອັກສອນ_ຂໍ້ມູນ', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
