#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/통신다리.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('통신다리', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('통신다리')
    대응 = {'response': '응답자료', 'parts': 'yo_l_tarkibiy_qism', 's': 'satr_ma_lumotlar', 'i': '순번', 'close': 'Yopish', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'kiritish_VALUE', 'flags': 'tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati', 'ftp_port': '파일전송접속번호', 'args': 'dalil_ARRAY', 'server': 'server_VALUE', 'data': 'ma_lumotlar', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'filtr_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'tashkilotchi', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'mehmon', 'destination': 'ko_chirish_joyi_ma_lumotlar_manzil', 'ethernet_port': 'Ethernet_port', 'b': 'SECOND_VALUE', 'MAC': '기계주소', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Davr_VALUE', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'belgi_kodi', 'p': 'ma_lumotlar_holat', 'writers': '쓰기대상들', 'IP': 'Internetdagi_manzil_VALUE', 'e': '보조항목', 'n': 'element_COUNT', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': '통신다리', 'window': 'oyna', 'capture': 'olish'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
