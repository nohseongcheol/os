#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/Mtandao_daraja.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('Mtandao_daraja', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Mtandao_daraja')
    대응 = {'response': '응답자료', 'parts': 'njia_kijenzi', 's': 'tungo_data', 'i': '순번', 'close': 'funga', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ingizo_thamani', 'flags': 'usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma', 'ftp_port': 'faili_hamisha_namba_ya_kituo', 'args': 'hoja_ARRAY', 'server': 'seva_thamani', 'data': 'data', 'ethernet_input': '이더넷입력', 'trace_packet': 'idadi_ya_maingizo_mlalo_pakiti', 'GATEWAY': '관문기계주소', 'rule': 'kanuni_thamani', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'mwenyeji', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'mgeni', 'destination': 'fikio_data_anwani', 'ethernet_port': 'Ethaneti_kituo', 'b': '둘째값', 'MAC': 'mashine_anwani', 'arp': 'anwani_mwonekano_pakiti', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Mzunguko_thamani', 'port': 'namba_ya_kituo', 'offset': 'Chipua_thamani', 'readable': '읽을수있음', 'c': 'msimbo_wa_kibambo', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'Anwani_tovuti_thamani', 'e': '보조항목', 'n': '개수', 'packet': 'pakiti_data', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Mtandao_daraja', 'window': 'dirisha', 'capture': 'unasaji'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
