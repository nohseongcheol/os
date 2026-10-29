#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/netwerk_pont.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('netwerk_pont', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('netwerk_pont')
    대응 = {'response': '응답자료', 'parts': 'mogħdija_komponent', 's': 'string_data', 'i': '순번', 'close': 'agħlaq', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'entrata_VALUE', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'argument_ARRAY', 'server': 'server_VALUE', 'data': 'data', 'ethernet_input': '이더넷입력', 'trace_packet': 'traċċar_pakkett', 'GATEWAY': '관문기계주소', 'rule': 'filtru_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'host', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'mistieden', 'destination': 'destinazzjoni_data_ADDRESS', 'ethernet_port': 'Ethernet_port', 'b': 'SECOND_VALUE', 'MAC': 'kompjuter_ADDRESS', 'arp': 'ADDRESS_riżoluzzjoni_pakkett', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Ċiklu_VALUE', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'kodiċi_tal_karattru', 'p': 'data_pożizzjoni', 'writers': '쓰기대상들', 'IP': 'indirizz_tal_Internet_VALUE', 'e': '보조항목', 'n': 'element_COUNT', 'packet': 'pakkett_data', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'netwerk_pont', 'window': 'tieqa', 'capture': 'iġbed'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
