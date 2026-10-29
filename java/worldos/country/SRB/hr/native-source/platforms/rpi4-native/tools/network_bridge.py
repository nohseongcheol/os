#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/most_3de4fe3a.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('most_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('most_3de4fe3a')
    mapiranje_VALUE = {'response': 'odgovor_1262b476', 'parts': 'put_komponenta', 's': 'niz_podaci', 'i': '순번', 'close': 'Zatvori', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'unos_VALUE', 'flags': 'konfiguracija_Pozadinski_pametni_servis_za_transfer', 'ftp_port': 'prijenos_datoteka_broj_priključka', 'args': 'argument_ARRAY', 'server': 'server_VALUE', 'data': 'podaci', 'ethernet_input': '이더넷입력', 'trace_packet': 'trag_paket', 'GATEWAY': '관문기계주소', 'rule': 'filtar_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'domaćin', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'gost', 'destination': 'odredište_podaci_adresa', 'ethernet_port': 'priključak_za_Ethernet', 'b': 'SECOND_VALUE', 'MAC': 'apsolutna_adresa', 'arp': 'adresa_razlučivost_paket', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Ciklus_VALUE', 'port': 'broj_priključka', 'offset': 'pomak_VALUE', 'readable': '읽을수있음', 'c': 'kodna_točka', 'p': 'podaci_položaj', 'writers': '쓰기대상들', 'IP': 'internetska_adresa_VALUE', 'e': '보조항목', 'n': 'artikl_COUNT', 'packet': 'paket_podaci', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'most_3de4fe3a', 'window': 'Prozor', 'capture': 'snimiti'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
