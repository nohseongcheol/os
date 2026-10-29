#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/brygga_3de4fe3a.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('brygga_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('brygga_3de4fe3a')
    mappning_värde = {'response': 'svar', 'parts': 'väg_komponent', 's': 'sträng_data', 'i': '순번', 'close': 'Stäng', 'forward': '전달규칙', 'slip_input': 'Serial_Line_Internet_Protocol_indata', 'self': '자신', 'item': 'post_värde', 'flags': 'konfiguration_BITS', 'ftp_port': 'filöverföring_portnummer', 'args': 'argument_MATRIS', 'server': 'server_värde', 'data': 'data', 'ethernet_input': 'Ethernet_indata', 'trace_packet': 'spår_paket', 'GATEWAY': 'gateway_maskinvara_ADRESS', 'rule': 'linje_värde', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'värd', 'ack': '확인번호', 'serial_port': 'seriell_port_nummer', 'readers': '읽기대상들', 'guest': 'gäst', 'destination': 'mål_data_ADRESS', 'ethernet_port': 'Ethernet_port', 'b': 'SEKUND_värde', 'MAC': 'absolut_adress', 'arp': 'ADRESS_upplösning_paket', 'writable': 'skrivbar', 'direction': '방향', 'seq': 'order_nummer', 'frame': 'körning_ram', 'loop': 'cykel_värde', 'port': 'portnummer', 'offset': 'FÖRSKJUTNING_värde', 'readable': '읽을수있음', 'c': 'kodpunkt', 'p': 'data_placera', 'writers': '쓰기대상들', 'IP': 'Internetadress_värde', 'e': '보조항목', 'n': 'objekt_ANTAL', 'packet': 'paket_data', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'brygga_3de4fe3a', 'window': 'Fönster', 'capture': 'Capture'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
