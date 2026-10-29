#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/mrežni_most.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('mrežni_most', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('mrežni_most')
    mapiranje_VALUE = {'response': 'odgovor_1262b476', 'parts': 'putanja_komponenta', 's': 'niska_podaci', 'i': '순번', 'close': 'Zatvori', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'stavka_VALUE', 'flags': 'konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini', 'ftp_port': 'prenos_datoteka_broj_porta', 'args': 'argument_niz', 'server': 'server_VALUE', 'data': 'podaci', 'ethernet_input': '이더넷입력', 'trace_packet': 'trag_paket', 'GATEWAY': '관문기계주소', 'rule': 'filter_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'host', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'gost', 'destination': 'odredište_podaci_adresa', 'ethernet_port': 'Ethernet_port', 'b': 'SECOND_VALUE', 'MAC': 'apsolutna_adresa', 'arp': 'adresa_rezolucija_paket', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Ciklus_VALUE', 'port': 'broj_porta', 'offset': 'Pomak_VALUE', 'readable': '읽을수있음', 'c': 'kôd_znaka', 'p': 'podaci_pozicija', 'writers': '쓰기대상들', 'IP': 'Internet_adresa_VALUE', 'e': '보조항목', 'n': 'stavka_COUNT', 'packet': 'paket_podaci', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'mrežni_most', 'window': 'prozor', 'capture': 'uhvatiti'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
