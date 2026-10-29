#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/most_3de4fe3a.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('most_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('most_3de4fe3a')
    대응 = {'response': 'odpověď', 'parts': 'cesta_součást', 's': 'řetězec_data', 'i': '순번', 'close': 'Zavřené', 'forward': '전달규칙', 'slip_input': 'protokol_SLIP_vstup', 'self': '자신', 'item': 'položka_HODNOTA', 'flags': 'konfigurace_BITS', 'ftp_port': 'přenos_souborů_číslo_portu', 'args': 'argument_pole', 'server': 'server_HODNOTA', 'data': 'data', 'ethernet_input': 'síť_Ethernet_vstup', 'trace_packet': 'stopa_paket', 'GATEWAY': 'brána_hardware_ODKAZ', 'rule': 'filtr_HODNOTA', 'protocol': 'síť_ABI', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'hostit', 'ack': '확인번호', 'serial_port': 'port_COM_číslo', 'readers': '읽기대상들', 'guest': 'host', 'destination': 'cíl_data_ODKAZ', 'ethernet_port': 'port_sítě_Ethernet', 'b': 'SEKUNDA_HODNOTA', 'MAC': 'absolutní_adresa', 'arp': 'ODKAZ_řešení_paket', 'writable': 'zapisovatelný', 'direction': '방향', 'seq': 'pořadí_číslo', 'frame': 'spuštění_rámec', 'loop': 'Cyklus_HODNOTA', 'port': 'číslo_portu', 'offset': 'POSUN_HODNOTA', 'readable': '읽을수있음', 'c': 'bod_kódu', 'p': 'data_pozice', 'writers': '쓰기대상들', 'IP': 'internetová_adresa_HODNOTA', 'e': '보조항목', 'n': 'zboží_POČET', 'packet': 'paket_data', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'most_3de4fe3a', 'window': 'Okno', 'capture': 'čerpat'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
