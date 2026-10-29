#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/brug_3de4fe3a.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('brug_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('brug_3de4fe3a')
    toewijzing_WAARDE = {'response': 'reactie_1262b476', 'parts': 'pad_onderdeel', 's': 'tekenreeks_gegevens', 'i': '순번', 'close': 'Sluiten', 'forward': '전달규칙', 'slip_input': 'Serial_Line_Internet_Protocol_invoer', 'self': '자신', 'item': 'invoer_WAARDE_962f286b', 'flags': 'configuratie_BITS', 'ftp_port': 'bestandsoverdracht_poortnummer', 'args': 'argument_MATRIX', 'server': 'server_WAARDE', 'data': 'gegevens', 'ethernet_input': 'Ethernet_invoer', 'trace_packet': 'spoor_pakket', 'GATEWAY': 'gateway_hardware_ADRES', 'rule': 'regel_WAARDE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'host', 'ack': '확인번호', 'serial_port': 'COM_poort_nummer', 'readers': '읽기대상들', 'guest': 'gast', 'destination': 'doel_gegevens_ADRES', 'ethernet_port': 'ethernet_poort', 'b': 'SECONDE_WAARDE', 'MAC': 'absoluut_adres', 'arp': 'ADRES_resolutie_pakket', 'writable': 'schrijfbaar', 'direction': '방향', 'seq': 'order_nummer', 'frame': 'uitvoerbewerking_frame', 'loop': 'cyclus_WAARDE', 'port': 'poortnummer', 'offset': 'VERSCHUIVING_WAARDE', 'readable': '읽을수있음', 'c': 'codepoint', 'p': 'gegevens_functie', 'writers': '쓰기대상들', 'IP': 'internetadres_WAARDE', 'e': '보조항목', 'n': 'item_AANTAL', 'packet': 'pakket_gegevens', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'brug_3de4fe3a', 'window': 'Venster', 'capture': 'Capture'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
