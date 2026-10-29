#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/Netwerk_brug.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('Netwerk_brug', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Netwerk_brug')
    대응 = {'response': '응답자료', 'parts': 'pad_komponent', 's': 'string_data', 'i': '순번', 'close': 'Sluit', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'inskrywing_VALUE', 'flags': 'konfigurasie_Agtergrond_intelligente_oordragdiens', 'ftp_port': '파일전송접속번호', 'args': 'argument_ARRAY', 'server': 'bediener_VALUE', 'data': 'data', 'ethernet_input': '이더넷입력', 'trace_packet': 'spoor_pakket', 'GATEWAY': 'deurgang_hardeware_adres', 'rule': 'reël_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'hou', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'gas', 'destination': 'bestemming_data_adres', 'ethernet_port': 'Eternetpoort', 'b': 'SECOND_VALUE', 'MAC': 'masjien_adres', 'arp': 'adres_resolusie_pakket', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Siklus_VALUE', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'karakterkode', 'p': 'data_plaas', 'writers': '쓰기대상들', 'IP': 'internetadres_VALUE', 'e': '보조항목', 'n': 'item_COUNT', 'packet': 'pakket_data', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Netwerk_brug', 'window': 'venster', 'capture': 'lê_vas'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
