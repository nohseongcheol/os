#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/Mreža_most.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('Mreža_most', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Mreža_most')
    대응 = {'response': '응답자료', 'parts': 'put_komponenta', 's': 'string_podaci', 'i': '순번', 'close': 'Zatvori', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'unos_VALUE', 'flags': '설정비트', 'ftp_port': 'fajl_prijenos_broj_priključka', 'args': 'argument_niz', 'server': 'server_VALUE', 'data': 'podaci', 'ethernet_input': '이더넷입력', 'trace_packet': 'trag_paket', 'GATEWAY': 'pristupni_uređaj_hardver_adresa', 'rule': 'filter_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'organizator', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'gost', 'destination': 'odredište_podaci_adresa', 'ethernet_port': 'priključak_za_Ethernet', 'b': 'SECOND_VALUE', 'MAC': 'mašina_adresa', 'arp': 'adresa_rezolucija_paket', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'krug_VALUE', 'port': 'broj_priključka', 'offset': 'Pomak_VALUE', 'readable': '읽을수있음', 'c': 'kôd_znaka', 'p': 'podaci_položaj', 'writers': '쓰기대상들', 'IP': 'internetska_adresa_VALUE', 'e': '보조항목', 'n': 'stavka_COUNT', 'packet': 'paket_podaci', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Mreža_most', 'window': 'prozor', 'capture': 'snimiti'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
