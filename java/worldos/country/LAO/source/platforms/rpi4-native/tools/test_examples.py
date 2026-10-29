#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/예제시험.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'ຟາຍ_ໂອນ_ຫມາຍເລກພອດ', 'data': 'ຂໍ້ມູນ', 'graphics_command': 'ກຣາບຟິກ_ຄໍາສັ່ງ', 'main': 'ແລ່ນ', 'row': 'ແຖວ_ຈັດຕໍາແຫນ່ງ', 'init': '초기값', 'target': 'ເປົ້າ_ຫມາຍ', 'ROOT': 'ໂຄງ_ການ_ເລກຮາກ', 'text': 'ຂໍ້ຄວາມ', 'binary': 'ຖານ_ສອງ', 'out': 'ມາດຕະການ_ຂໍ້ມູນ', 'entry': 'ເຂົ້າໃນ_ຈຸດ', 'got': '받은수', 'port': 'ຫມາຍເລກພອດ', 'graphics_start': 'ເລີ່ມ_ການ_ແຕ້ມ', 'col': 'ຖັນ_ຈັດຕໍາແຫນ່ງ', 'begin': 'ເລີ່ມ_ອອບເຊັດ', 'kind': 'ຫມວດ_ຄ່າ', 'selector': 'ຕົວ_ໃຊ້_ເລືອກ', 'n': '개수', 'key': '누름값', 'y': 'ປຸ່ມ_Y_ຈຸດປະສານ', 'client': 'ລູກຂ່າຍ', 'line': 'ສາຍ', 'report': 'ໃຊ້ໄດ້_ລາຍງານ', 'language': 'ພາ_ສາ', 'x': 'ຈຸດ_ພິ_ກັດ_x', 'start': 'ແລ່ນ', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'ສົ່ງ_ລາຍຊື່', 'payload': 'ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ', 'proc': 'ຂະ_ບວນ_ການ', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ຊື່_ຕາຕະລາງ', 'content': 'ເນື້ອໃນ_ຄ່າ_cb0f2404', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ຟາຍ_ເຂົ້າໃນ_ຊື່', 'shell': 'ເຊລ', 'color': '색상', 'transcript': '대화기록', 'offset': 'ອອບເຊັດ_ຄ່າ', 'h': '높이값', 'run': 'ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ', 'c': 'ຈຸດ_ລະ_ຫັດ', 'path': 'ທາງໂຄຈອນ', 'encoding': 'ຊຸດ_ຕົວ_ອັກ_ສອນ', 'end': 'ຈົບ_ອອບເຊັດ', 'ftp': 'ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່', 'pixels': '화소들', 'symbol': 'ສັນຍາລັກ_ຄ່າ', 'source': '원본자료', 'name': 'ຊື່', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
