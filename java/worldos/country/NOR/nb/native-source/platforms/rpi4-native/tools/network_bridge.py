#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/bro_3de4fe3a.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('bro_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('bro_3de4fe3a')
    tildeling_VERDI = {'response': 'svar_1262b476', 'parts': 'bane_komponent', 's': 'streng_data', 'i': '순번', 'close': 'Lukk', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'oppføring_VERDI', 'flags': 'konfigurasjon_BITS', 'ftp_port': 'filoverføring_portnummer', 'args': 'argument_MATRISE', 'server': 'server_VERDI', 'data': 'data', 'ethernet_input': 'Ethernet_inndata', 'trace_packet': 'spor_pakke', 'GATEWAY': 'gateway_maskinvare_e_post', 'rule': 'regel_VERDI', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'vert', 'ack': '확인번호', 'serial_port': 'COM_port_nummer', 'readers': '읽기대상들', 'guest': 'gjest', 'destination': 'mål_data_e_post', 'ethernet_port': 'Ethernet_port', 'b': 'SEKUND_VERDI', 'MAC': 'absolutt_adresse', 'arp': 'e_post_oppløsning_pakke', 'writable': '쓸수있음', 'direction': '방향', 'seq': 'ordre_nummer', 'frame': 'kjøring_bilde', 'loop': 'Krets_VERDI', 'port': 'portnummer', 'offset': 'FORSKYVNING_VERDI', 'readable': '읽을수있음', 'c': 'tegnkode', 'p': 'data_plassere', 'writers': '쓰기대상들', 'IP': 'Internett_adresse_VERDI', 'e': '보조항목', 'n': 'vare_ANTALL', 'packet': 'pakke_data', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'bro_3de4fe3a', 'window': 'Vindu', 'capture': 'hente'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
