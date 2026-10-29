#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/sieťový_most.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('sieťový_most', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('sieťový_most')
    mapovanie_VALUE = {'response': 'odpoveď', 'parts': 'cesta_súčasť', 's': 'reťazec_údaje', 'i': '순번', 'close': 'Zatvoriť', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'položka_VALUE', 'flags': 'konfigurácia_Background_Intelligent_Transfer_Service', 'ftp_port': 'prenos_súborov_číslo_portu', 'args': 'argument_pole', 'server': 'server_VALUE', 'data': 'údaje', 'ethernet_input': 'sieť_Ethernet_vstup', 'trace_packet': 'sledovať_paket', 'GATEWAY': 'brána_hardvér_adresa', 'rule': 'filter_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'hostiteľ', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'hosť', 'destination': 'cieľ_údaje_adresa', 'ethernet_port': 'port_Ehternet', 'b': 'SECOND_VALUE', 'MAC': 'absolútna_adresa', 'arp': 'adresa_rozlíšenie_paket', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Cyklus_VALUE', 'port': 'číslo_portu', 'offset': 'Posun_VALUE', 'readable': '읽을수있음', 'c': 'bod_kódu', 'p': 'údaje_pozícia', 'writers': '쓰기대상들', 'IP': 'internetová_adresa_VALUE', 'e': '보조항목', 'n': 'položka_COUNT', 'packet': 'paket_údaje', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'sieťový_most', 'window': 'Okno', 'capture': 'snímať'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
