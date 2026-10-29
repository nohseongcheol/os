#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/bro_3de4fe3a.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('bro_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('bro_3de4fe3a')
    tilknytning_VÆRDI = {'response': 'svar_1262b476', 'parts': 'sti_komponent', 's': 'streng_data', 'i': '순번', 'close': 'Luk', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'post_VÆRDI_962f286b', 'flags': 'konfiguration_BITS', 'ftp_port': 'filoverførsel_portnummer', 'args': 'argument_MATRIX', 'server': 'server_VÆRDI', 'data': 'data', 'ethernet_input': 'Ethernet_input', 'trace_packet': 'spor_pakke', 'GATEWAY': 'gateway_hardware_mail', 'rule': 'regel_VÆRDI', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'vært', 'ack': '확인번호', 'serial_port': 'COM_port_tal', 'readers': '읽기대상들', 'guest': 'gæst', 'destination': 'destination_data_mail', 'ethernet_port': 'Ethernet_port', 'b': 'SEKUND_VÆRDI', 'MAC': 'absolut_adresse', 'arp': 'mail_opløsning_pakke', 'writable': 'skrivbar', 'direction': '방향', 'seq': 'ordre_tal', 'frame': 'udførelse_ramme', 'loop': 'Cyklus_VÆRDI', 'port': 'portnummer', 'offset': 'FORSKYDNING_VÆRDI', 'readable': '읽을수있음', 'c': 'tegnkode', 'p': 'data_placere', 'writers': '쓰기대상들', 'IP': 'internetadresse_VÆRDI', 'e': '보조항목', 'n': 'vare_TÆL', 'packet': 'pakke_data', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'bro_3de4fe3a', 'window': 'Vindue', 'capture': 'optage'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
