#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/Net_brú.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('Net_brú', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Net_brú')
    vörpun_VALUE = {'response': '응답자료', 'parts': 'slóð_þáttur', 's': 'strengur_gögn', 'i': '순번', 'close': 'Loka', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'færsla_VALUE', 'flags': 'afbrigði_Background_Intelligent_Transfer_Service', 'ftp_port': 'skrá_flytja_tengisnúmer', 'args': 'frumbreyta_ARRAY', 'server': 'þjónn_VALUE', 'data': 'gögn', 'ethernet_input': '이더넷입력', 'trace_packet': 'spor_pakki', 'GATEWAY': '관문기계주소', 'rule': 'sía_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'hýsa', 'ack': '확인번호', 'serial_port': 'raðtengi_númer', 'readers': '읽기대상들', 'guest': 'gestur', 'destination': 'endastaður_gögn_slóð', 'ethernet_port': 'Íðnetstengi', 'b': 'SECOND_VALUE', 'MAC': 'vél_slóð', 'arp': 'slóð_upplausn_pakki', 'writable': '쓸수있음', 'direction': '방향', 'seq': 'röð_númer', 'frame': '실행틀', 'loop': 'lota_VALUE', 'port': 'tengisnúmer', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'stafkóði', 'p': 'gögn_staða', 'writers': '쓰기대상들', 'IP': 'veffang_VALUE', 'e': '보조항목', 'n': 'vara_COUNT', 'packet': 'pakki_gögn', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Net_brú', 'window': 'Gluggi', 'capture': 'fanga'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
