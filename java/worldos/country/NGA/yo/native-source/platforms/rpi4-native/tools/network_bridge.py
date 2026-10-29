#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/Alásopọ̀_afará.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('Alásopọ̀_afará', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Alásopọ̀_afará')
    대응 = {'response': '응답자료', 'parts': 'ọ̀nà_ẹ̀yà', 's': 'fọ́nrán_détà', 'i': '순번', 'close': 'Ti', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ìgbéwọlé_iye', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'ágúmẹ́ntì_ÀRÉÈ', 'server': 'apèsè_iye', 'data': 'détà', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': 'ẹnu_odi_ohun_èlò_alárídìmú_àdírẹ́ẹ̀sì', 'rule': 'asẹ́_iye', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'olùpèsè', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'àlejò', 'destination': 'èbúté_détà_àdírẹ́ẹ̀sì', 'ethernet_port': 'Ethernet_ojú', 'b': '둘째값', 'MAC': 'àdírẹ́ẹ̀sì_maṣíìnì', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Ìpòyì_iye', 'port': '접속번호', 'offset': 'Ìtayọ_iye', 'readable': '읽을수있음', 'c': 'kóòdù_ẹyọ_ọ̀rọ̀', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'àdíréẹ̀sì_íntánẹ́ẹ̀tì_iye', 'e': '보조항목', 'n': '개수', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Alásopọ̀_afará', 'window': 'wínńdò', 'capture': 'gbàwòránsílẹ̀'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
