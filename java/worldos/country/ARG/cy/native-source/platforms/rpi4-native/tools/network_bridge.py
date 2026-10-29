#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/Rhwydwaith_pont.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('Rhwydwaith_pont', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Rhwydwaith_pont')
    대응 = {'response': '응답자료', 'parts': 'llwybr_cydran', 's': 'testun_data', 'i': '순번', 'close': 'Cau', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'cofnod_VALUE', 'flags': '설정비트', 'ftp_port': 'ffeil_trosglwyddo_rhif_porth', 'args': 'arg_ARAE', 'server': 'gweinydd_VALUE', 'data': 'data', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'hidlo_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'lletya', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'gwestai', 'destination': 'cyrchfan_data_ADDRESS', 'ethernet_port': 'porth_ether_rwyd', 'b': 'SECOND_VALUE', 'MAC': 'peiriant_ADDRESS', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Cylch_VALUE', 'port': 'rhif_porth', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'cod_nod', 'p': 'data_safle', 'writers': '쓰기대상들', 'IP': 'cyfeiriad_rhyngrwyd_VALUE', 'e': '보조항목', 'n': 'eitem_COUNT', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Rhwydwaith_pont', 'window': 'ffenestr', 'capture': 'recordio'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
