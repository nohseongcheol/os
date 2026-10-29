#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/Reseau_Bréck.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('Reseau_Bréck', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Reseau_Bréck')
    대응 = {'response': '응답자료', 'parts': 'Wee_Komponent', 's': 'Zeechefolleg_Daten', 'i': '순번', 'close': 'Clôture', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'Agab_VALUE', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'Argument_ARRAY', 'server': 'Server_VALUE', 'data': 'Daten', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'Regel_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'Host', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'Gaascht', 'destination': 'Zil_Daten_Adress', 'ethernet_port': 'Ethernet_Port', 'b': 'SECOND_VALUE', 'MAC': 'Computer_Adress', 'arp': 'Adress_Opléisung_Pak', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Zyklus_VALUE', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'Zeechecode', 'p': 'Daten_positionéieren', 'writers': '쓰기대상들', 'IP': 'Internetsadress_VALUE', 'e': '보조항목', 'n': 'Element_COUNT', 'packet': 'Pak_Daten', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Reseau_Bréck', 'window': 'Fënster', 'capture': 'ophuelen'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
