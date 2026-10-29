#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/Nettverk_bru.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('Nettverk_bru', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Nettverk_bru')
    대응 = {'response': '응답자료', 'parts': 'bane_komponent', 's': 'streng_data', 'i': '순번', 'close': 'Lukk', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'oppføring_VALUE', 'flags': '설정비트', 'ftp_port': 'fil_Overfør_portnummer', 'args': 'argument_ARRAY', 'server': 'tenar_VALUE', 'data': 'data', 'ethernet_input': '이더넷입력', 'trace_packet': 'spor_pakke', 'GATEWAY': '관문기계주소', 'rule': 'regel_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'vert', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'gjest', 'destination': 'mål_data_ADDRESS', 'ethernet_port': 'Ethernet_port', 'b': 'SECOND_VALUE', 'MAC': 'maskin_ADDRESS', 'arp': 'ADDRESS_oppløysing_pakke', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Syklus_VALUE', 'port': 'portnummer', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'teiknkode', 'p': 'data_plassere', 'writers': '쓰기대상들', 'IP': 'Internett_adresse_VALUE', 'e': '보조항목', 'n': 'vare_COUNT', 'packet': 'pakke_data', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Nettverk_bru', 'window': 'vindauge', 'capture': 'ta_opp'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
