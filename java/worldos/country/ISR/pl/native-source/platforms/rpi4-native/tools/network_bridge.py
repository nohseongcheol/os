#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/mostek_3de4fe3a.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('mostek_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('mostek_3de4fe3a')
    mapowanie_WARTOŚĆ = {'response': 'odpowiedź_1262b476', 'parts': 'ścieżka_składnik', 's': 'ciąg_dane', 'i': '순번', 'close': 'Zamknięte', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'wpis_WARTOŚĆ', 'flags': 'konfiguracja_BITS', 'ftp_port': 'transfer_plików_numer_portu', 'args': 'argument_TABLICA', 'server': 'serwer_WARTOŚĆ', 'data': 'dane', 'ethernet_input': 'Ethernet_wejście', 'trace_packet': 'ślad_pakiet', 'GATEWAY': 'brama_sprzęt_ADRES', 'rule': 'filtr_WARTOŚĆ', 'protocol': 'sieć_ABI', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'host', 'ack': '확인번호', 'serial_port': 'port_COM_identyfikator', 'readers': '읽기대상들', 'guest': 'gość', 'destination': 'cel_dane_ADRES', 'ethernet_port': 'port_Ethernet', 'b': 'SEKUNDA_WARTOŚĆ', 'MAC': 'adres_bezwzględny', 'arp': 'ADRES_rozdzielczość_pakiet', 'writable': 'zapisywalny', 'direction': '방향', 'seq': 'zamówić_identyfikator', 'frame': 'wykonanie_kadr', 'loop': 'Cykl_WARTOŚĆ', 'port': 'numer_portu', 'offset': 'przesunąć_WARTOŚĆ_450fc799', 'readable': '읽을수있음', 'c': 'kod_znaku', 'p': 'dane_stanowisko', 'writers': '쓰기대상들', 'IP': 'adres_internetowy_WARTOŚĆ', 'e': '보조항목', 'n': 'towar_ILE_LICZB', 'packet': 'pakiet_dane', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'mostek_3de4fe3a', 'window': 'Okno', 'capture': 'Capture'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
