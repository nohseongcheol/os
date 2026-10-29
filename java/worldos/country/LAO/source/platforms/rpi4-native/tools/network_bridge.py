#!/usr/bin/env python3
"""기존 ທາງໂຄຈອນ 호환 ເຂົ້າໃນ_ຈຸດ. ຕົວ_ຈິງ_ຂໍ້ມູນ 구현: ../ເຄື່ອງມື/ເຄືອຂ່າຍ_ຕົວເຊື່ອມ.py"""
import importlib as 가져오기
import sys as ລະບົບປະຕິບັດການ_ຄ່າ
from pathlib import Path as ທາງໂຄຈອນ
ລະບົບປະຕິບັດການ_ຄ່າ.path.insert(0, str(ທາງໂຄຈອນ(__file__).resolve().parents[1] / 'ເຄື່ອງມື'))
if __name__ == '__main__':
    import runpy as ແອັບ_ຕົວເປີດໃຊ້
    ແອັບ_ຕົວເປີດໃຊ້.run_module('ເຄືອຂ່າຍ_ຕົວເຊື່ອມ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ເຄືອຂ່າຍ_ຕົວເຊື່ອມ')
    대응 = {'response': '응답자료', 'parts': 'ທາງໂຄຈອນ_ອົງປະກອບ', 's': 'ສະຕຣິງ_ຂໍ້ມູນ', 'i': '순번', 'close': 'ປິດ', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ເຂົ້າໃນ_ຄ່າ', 'flags': 'ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ', 'ftp_port': 'ຟາຍ_ໂອນ_ຫມາຍເລກພອດ', 'args': 'ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ', 'server': '서버', 'data': 'ຂໍ້ມູນ', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'ລະບຽບ_ຄ່າ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'ໂຮສ', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'ແຂກ', 'destination': 'ປາຍທາງ_ຂໍ້ມູນ_ອີເມວ', 'ethernet_port': 'ການເຊື່ອມຕໍ່ແບບຜ່ານສາຍ_ຜອດ', 'b': '둘째값', 'MAC': 'ເຄື່ອງຈັກ_ອີເມວ', 'arp': 'ອີເມວ_ຄວາມລະອຽດ_ແພັກເກັດ', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'ຮອບ_ຄ່າ', 'port': 'ຫມາຍເລກພອດ', 'offset': 'ອອບເຊັດ_ຄ່າ', 'readable': '읽을수있음', 'c': 'ຈຸດ_ລະ_ຫັດ', 'p': 'ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ', 'writers': '쓰기대상들', 'IP': 'ທີ່ຢູ່ອິນເຕີເນັດ_ຄ່າ', 'e': '보조항목', 'n': '개수', 'packet': 'ແພັກເກັດ_ຂໍ້ມູນ', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'ເຄືອຂ່າຍ_ຕົວເຊື່ອມ', 'window': 'ວິນໂດ', 'capture': 'ບັນທຶກ_ba7b8054'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
