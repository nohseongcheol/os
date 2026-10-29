#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/tilts_3de4fe3a.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('tilts_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('tilts_3de4fe3a')
    kartēšana_VALUE = {'response': 'atbilde_1262b476', 'parts': 'ceļš_komponents', 's': 'virkne_dati', 'i': '순번', 'close': 'Aizvērt', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ievade_VALUE', 'flags': 'konfigurācija_Background_Intelligent_Transfer_Service', 'ftp_port': 'faila_pārsūtīšana_porta_numurs', 'args': 'arg_ARRAY', 'server': 'serveris_VALUE', 'data': 'dati', 'ethernet_input': '이더넷입력', 'trace_packet': 'pēda_pakete', 'GATEWAY': '관문기계주소', 'rule': 'filtrs_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'viesot', 'ack': '확인번호', 'serial_port': 'COM_ports_numurs', 'readers': '읽기대상들', 'guest': 'viesis', 'destination': 'mērķis_dati_adrese', 'ethernet_port': 'Ethernet_ports', 'b': 'SECOND_VALUE', 'MAC': 'reālā_adrese', 'arp': 'adrese_izšķirtspēja_pakete', 'writable': '쓸수있음', 'direction': '방향', 'seq': 'secība_numurs', 'frame': '실행틀', 'loop': 'Cikls_VALUE', 'port': 'porta_numurs', 'offset': 'Nobīde_VALUE', 'readable': '읽을수있음', 'c': 'koda_punkts', 'p': 'dati_amats', 'writers': '쓰기대상들', 'IP': 'interneta_adrese_VALUE', 'e': '보조항목', 'n': 'krājums_COUNT', 'packet': 'pakete_dati', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'tilts_3de4fe3a', 'window': 'Logs', 'capture': 'tvert'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
