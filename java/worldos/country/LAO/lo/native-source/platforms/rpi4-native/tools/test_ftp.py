#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/파일전송시험.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ຂໍ້ມູນ', 'proc': 'ຂະ_ບວນ_ການ', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'ການສໍາເນົາ', 'main': 'ແລ່ນ', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'ກໍານົດເອງ_ແຫຼ່ງທີ່ມາ', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'ໂຄງ_ການ_ເລກຮາກ', 'text': 'ຂໍ້ຄວາມ', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'ຄໍາສັ່ງ_1f12b8e2', 'out': 'ມາດຕະການ_ຂໍ້ມູນ', 'expected': '예상결과', 'server_source': '서버원문', 'shell': 'ເຊລ', 'upload': 'ໂອນອອກ_ໄຟລ໌', 'transcript': '대화기록', 'port': 'ຫມາຍເລກພອດ', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ຕົວເຊື່ອມ', 'selector': 'ຕົວ_ໃຊ້_ເລືອກ', 'end': 'ຈົບ_ອອບເຊັດ', 'e': '보조항목', 'ftp': 'ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'ລຸ້ນດຽວກັນ_ຄ່າ', 'result': 'ມາດຕະການ', 'unchanged': '보존자료', 'line': 'ສາຍ', 'server_tcp_port': '서버연결접속번호', 'source': '원본자료', 'NetworkBridge': 'ເຄືອຂ່າຍ_ຕົວເຊື່ອມ', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'ໃຊ້ໄດ້_ລາຍງານ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
