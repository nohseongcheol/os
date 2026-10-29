#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/부팅시험.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'ເຄືອຂ່າຍ_ອີເມວ', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'ປະ_ຕິ_ບັດ_ຫນ້າວຽກ', 'cancel': 'ຍົກເລີກ_ການຄໍານວນ', 'cmd_byte': 'ຄໍາສັ່ງ_ໄບ', 'reply': 'ຕອບກັບ', 'points': '지점들', 'server': '서버', 'data': 'ຂໍ້ມູນ', 'prompt': 'ພຣອມ', 'enter': 'ປ້ອນ_ເຂົ້າ', 'imported': '들여온파일', 'send': 'ສົ່ງ', 'main': 'ແລ່ນ', 'ROOT': 'ໂຄງ_ການ_ເລກຮາກ', 'text': 'ຂໍ້ຄວາມ', 'first_gui': '첫화면', 'pixel': 'ເປ_ລ', 'java_class': '자바클래스', 'upload': 'ໂອນອອກ_ໄຟລ໌', 'pixels_file': 'ເປ_ລ_ຟາຍ', 'pixels_data': 'ເປ_ລ_ຂໍ້ມູນ', 'edit': 'ແກ້ໄຂ_ຄ່າ', 'receive_until': '표시까지받기', 'selector': 'ຕົວ_ໃຊ້_ເລືອກ', 'size': 'ຂະ_ຫນາດ', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'ປຸ່ມ_Y_ຈຸດປະສານ', 'result': 'ມາດຕະການ', 'samples': '예제들', 'client': 'ລູກຂ່າຍ', 'line': 'ສາຍ', 'report': 'ໃຊ້ໄດ້_ລາຍງານ', 'work': '작업경로', 'x': 'ຈຸດ_ພິ_ກັດ_x', 'python_checks': '파이썬검사', 'download': 'ດາວໂຫຼດ', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'ຂະ_ບວນ_ການ', 'content': 'ເນື້ອໃນ_ຄ່າ_cb0f2404', 'block': 'ຂໍ້ມູນ_ບລັອກ', 'marker': '확인표시', 'command': 'ຄໍາສັ່ງ_1f12b8e2', 'expected': '예상결과', 'shell': 'ເຊລ', 'drawing': 'ການ_ແຕ້ມ_ທາງໂຄຈອນ', 'f': 'ຟາຍ_ເຂົ້າໃນ', 'transcript': '대화기록', 'offset': 'ອອບເຊັດ_ຄ່າ', 'path': 'ທາງໂຄຈອນ', 'screenshot': 'ພາບຫນ້າຈໍ', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ສະຕຣີມ_ຄ່າ', 'cmd': '명령인수', 'name': 'ຊື່', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
