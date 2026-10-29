#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/ເດັສທັອບ_ເບິ່ງ.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('ເດັສທັອບ_ເບິ່ງ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ເດັສທັອບ_ເບິ່ງ')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'ຂໍ້ຜິດພາດ', 'exact': '정확한값', 'network': 'ເຄືອຂ່າຍ', 'closed': '닫힘', 'length': 'ຄວາມຍາວ_ຄ່າ', 'opened': '열림', 'ftp_port': 'ຟາຍ_ໂອນ_ຫມາຍເລກພອດ', 'server': '서버', 'resources': 'ແຫຼ່ງ_ຊັບ_ພະ_ຍາ_ກອນ', 'data': 'ຂໍ້ມູນ', 'shift': 'ປຸ່ມຊິບ', 'send': 'ສົ່ງ', 'run_desktop': 'ແລ່ນ_ເດັສທັອບ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'ໂຮສ', 'text': 'ຂໍ້ຄວາມ', 'korean': '한글여부', 'port': 'ຫມາຍເລກພອດ', 'signum': '신호번호', 'version': '판번호', 'parser': 'ຕົວແຍກວິເຄາະ', 'bridge': 'ຕົວເຊື່ອມ', 'kind': 'ຫມວດ_ຄ່າ', 'tail': '끝부분', 'size': 'ຂະ_ຫນາດ', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'ປຸ່ມ_Y_ຈຸດປະສານ', 'prefix': '앞부분', 'client': 'ລູກຂ່າຍ', 'char': 'ຕົວອັກສອນ_ຂໍ້ມູນ', 'work': '작업경로', 'Keyboard': 'ແປ້ນພິມ', 'x': 'ຈຸດ_ພິ_ກັດ_x', 'down': '누르는중', 'net': 'ເຄືອຂ່າຍ_ຕົວເຊື່ອມ_ເຂົ້າໃນ', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'ຂະ_ບວນ_ການ', 'Desktop': 'ເຊື່ອມຕໍ່_ເດັສທັອບ', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'ສະວິດ_ໂຫມດ', 'command': 'ຄໍາສັ່ງ_1f12b8e2', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'ຊີທີອາແອວ', 'path': 'ທາງໂຄຈອນ', 'cp': 'ຕົວອັກສອນ_ເຂົ້າລະຫັດ', 'terminate': '종료시키기', 'security': 'ຄວາມປອດໄພ', 'vnc_port': '원격화면접속번호', 'body': 'ເນື້ອໃນເອກະສານ', 'index': 'ຄົ້ນຫາ_ດັດຊະນີ', 'exited': '종료됨', 'keysym': 'ກະແຈ_ສັນຍາລັກ', 'output': '출력결과', 'keyboard': 'ແປ້ນພິມ_ເຂົ້າໃນ', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'ຜູ້ອ່ານ', 'NetworkBridge': 'ເຄືອຂ່າຍ_ຕົວເຊື່ອມ', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
