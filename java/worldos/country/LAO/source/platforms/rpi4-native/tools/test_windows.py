#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/창시험.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'ຈຸດ_ພິ_ກັດ_x', 's': 'ສະຕຣິງ_ຂໍ້ມູນ', 'xy': 'ຕົວປະສານຄູ່', 'sel': 'ຕົວ_ໃຊ້_ເລືອກ_a916db4e', 'seconds': '초단위', 'log': 'ບັນທຶກ_ແຖວ', 'at': '현재위치', 'send': 'ສົ່ງ', 'main': 'ແລ່ນ', 'req': '요청값', 'hot': 'ທາງລັດ_ຄ່າ', 'pump': 'ຈັດ_ການ_ງານ', 'ROOT': 'ໂຄງ_ການ_ເລກຮາກ', 'marker': '확인표시', 'b': '둘째값', 'command': 'ຄໍາສັ່ງ_1f12b8e2', 'shell': 'ເຊລ', 'f': 'ຟາຍ_ເຂົ້າໃນ', 'color': '색상', 'click': 'ກົດ_ປຸ່ມ', 'k': '셋째순번', 'c': 'ຈຸດ_ລະ_ຫັດ', 'r': '반환값', 'p': 'ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ', 'done': '완료량', 'end': 'ຈົບ_ອອບເຊັດ', 'command_mode': 'ຄໍາສັ່ງ_ໂຫມດ', 'key': '누름값', 'y': 'ປຸ່ມ_Y_ຈຸດປະສານ', 'pixels': '화소들', 'result': 'ມາດຕະການ', 'report': 'ໃຊ້ໄດ້_ລາຍງານ', 'dest': 'ປາຍທາງ_ຄ່າ_ຈັດຕໍາແຫນ່ງ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
