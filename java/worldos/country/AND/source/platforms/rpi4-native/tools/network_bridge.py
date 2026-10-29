#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/xarxa_pont.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('xarxa_pont', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('xarxa_pont')
    대응 = {'response': 'resposta_1262b476', 'parts': 'camí_component', 's': 'cadena_dades', 'i': '순번', 'close': 'Tanca', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'introducció_VALOR', 'flags': 'configuració_Servei_de_transferència_intel_ligent_en_segon_terme', 'ftp_port': 'transferència_de_fitxers_número_de_port', 'args': 'arg_MATRIU', 'server': 'servidor_VALOR', 'data': 'dades', 'ethernet_input': '이더넷입력', 'trace_packet': 'traça_paquet', 'GATEWAY': '관문기계주소', 'rule': 'regla_VALOR', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'allotjar', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'convidat', 'destination': 'destinació_dades_ADREÇA', 'ethernet_port': 'port_Ethernet', 'b': 'SEGON_VALOR', 'MAC': 'màquina_ADREÇA', 'arp': 'ADREÇA_resolució_paquet', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Cicle_VALOR', 'port': 'número_de_port', 'offset': 'DESPLAÇAMENT_VALOR', 'readable': '읽을수있음', 'c': 'codi_de_caràcter', 'p': 'dades_càrrec', 'writers': '쓰기대상들', 'IP': 'adreça_d_Internet_VALOR', 'e': '보조항목', 'n': 'element_COMPT', 'packet': 'paquet_dades', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'xarxa_pont', 'window': 'Finestra', 'capture': 'capturar'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
