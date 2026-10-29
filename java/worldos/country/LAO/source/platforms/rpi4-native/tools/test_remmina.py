#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/원격한글시험.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'ແລ່ນ', 'profile': 'ໂປຣໄຟລ໌', 'focused': 'ຮວມ', 'serial': '직렬입출력', 'keys': '누름열', 'server': '서버', 'log': 'ບັນທຶກ_ແຖວ', 'args': 'ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ', 'deadline': '마감시각', 'data': 'ຂໍ້ມູນ', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'ແລ່ນ', 'ready': '준비완료', 'found': 'ຊອກຫາ_ມາດຕະການ', 'guest': 'ແຂກ', 'ROOT': 'ໂຄງ_ການ_ເລກຮາກ', 'marker': '확인표시', 'text': 'ຂໍ້ຄວາມ', 'out': 'ມາດຕະການ_ຂໍ້ມູນ', 'env': '환경', 'f': 'ຟາຍ_ເຂົ້າໃນ', 'port': 'ຫມາຍເລກພອດ', 'offset': 'ອອບເຊັດ_ຄ່າ', 'version': '판번호', 'p': 'ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ', 'selector': 'ຕົວ_ໃຊ້_ເລືອກ', 'xvfb': 'ຈໍາລອງ_ສະແດງຜົນ', 'display': 'ສະແດງຜົນ', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'ຊື່', 'window': 'ວິນໂດ', 'report': 'ໃຊ້ໄດ້_ລາຍງານ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
