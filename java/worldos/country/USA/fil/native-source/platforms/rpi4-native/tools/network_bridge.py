#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/Network_bridge.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('Network_bridge', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Network_bridge')
    대응 = {'response': '응답자료', 'parts': 'path_component', 's': 'string_data', 'i': '순번', 'close': 'isara', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'pagpasok_VALUE', 'flags': 'kompigurasyon_Background_Intelligent_Transfer_Service', 'ftp_port': 'file_lipat_numero_ng_port', 'args': 'argumento_ARRAY', 'server': 'server_VALUE', 'data': 'data', 'ethernet_input': '이더넷입력', 'trace_packet': 'trace_packet', 'GATEWAY': '관문기계주소', 'rule': 'filter_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'host', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'bisita', 'destination': 'patutunguhan_data_email', 'ethernet_port': 'Ethernet_port', 'b': 'SECOND_VALUE', 'MAC': 'machine_email', 'arp': 'email_resolution_packet', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Cycle_VALUE', 'port': 'numero_ng_port', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'character_code', 'p': 'data_posisyon', 'writers': '쓰기대상들', 'IP': 'Internet_address_VALUE', 'e': '보조항목', 'n': 'item_COUNT', 'packet': 'packet_data', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Network_bridge', 'window': 'window', 'capture': 'mag_capture'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
