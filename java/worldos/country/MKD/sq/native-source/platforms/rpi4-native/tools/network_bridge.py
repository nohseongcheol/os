#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/rrjet_urë.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('rrjet_urë', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('rrjet_urë')
    대응 = {'response': 'përgjigje', 'parts': 'shteg_përbërës', 's': 'varg_të_dhëna', 'i': '순번', 'close': 'Mbyll', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'futje_VALUE', 'flags': 'konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond', 'ftp_port': 'skedar_transferim_numri_i_portës', 'args': 'argument_ARRAY', 'server': 'server_VALUE', 'data': 'të_dhëna', 'ethernet_input': '이더넷입력', 'trace_packet': 'gjurmë_paketë', 'GATEWAY': '관문기계주소', 'rule': 'filtër_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'pritës', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'i_ftuar', 'destination': 'vendmbërritje_të_dhëna_email', 'ethernet_port': 'fole_Ethernet', 'b': 'SECOND_VALUE', 'MAC': 'makinë_email', 'arp': 'email_rezolucion_paketë', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Cikël_VALUE', 'port': 'numri_i_portës', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'kodi_i_karakterit', 'p': 'të_dhëna_pozicioni', 'writers': '쓰기대상들', 'IP': 'adresë_në_internet_VALUE', 'e': '보조항목', 'n': 'njësi_COUNT', 'packet': 'paketë_të_dhëna', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'rrjet_urë', 'window': 'Dritare', 'capture': 'kap'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
