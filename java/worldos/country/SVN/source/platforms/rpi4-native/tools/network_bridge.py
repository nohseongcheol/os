#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/most_3de4fe3a.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('most_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('most_3de4fe3a')
    preslikava_VALUE = {'response': 'odziv', 'parts': 'pot_komponenta', 's': 'niz_podatki', 'i': '순번', 'close': 'Zapri', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'vnos_VALUE', 'flags': 'konfiguracija_storitev_Background_Intelligent_Transfer_Service', 'ftp_port': 'prenos_datotek_številka_vrat', 'args': 'argument_ARRAY', 'server': 'strežnik_VALUE', 'data': 'podatki', 'ethernet_input': '이더넷입력', 'trace_packet': 'sled_paket', 'GATEWAY': 'prehod_strojna_oprema_naslov', 'rule': 'filter_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'gostiti', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'gost', 'destination': 'cilj_podatki_naslov', 'ethernet_port': 'vrata_za_ethernet', 'b': 'SECOND_VALUE', 'MAC': 'absolutni_naslov', 'arp': 'naslov_ločljivost_paket', 'writable': 'zapisljiv', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Krog_VALUE', 'port': 'številka_vrat', 'offset': 'odmik_VALUE', 'readable': '읽을수있음', 'c': 'koda_znaka', 'p': 'podatki_položaj', 'writers': '쓰기대상들', 'IP': 'internetni_račun_VALUE', 'e': '보조항목', 'n': 'element_COUNT', 'packet': 'paket_podatki', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'most_3de4fe3a', 'window': 'okno', 'capture': 'snemati'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
