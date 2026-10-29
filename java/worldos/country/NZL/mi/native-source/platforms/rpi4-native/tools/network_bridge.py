#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/whatunga_arawhata.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('whatunga_arawhata', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('whatunga_arawhata')
    대응 = {'response': '응답자료', 'parts': 'ara_wae', 's': 'aho_raraunga', 'i': '순번', 'close': 'Kati', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'tāurunga_uara', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'tohenga_HUĀNGA', 'server': 'tūmau_uara', 'data': 'raraunga', 'ethernet_input': '이더넷입력', 'trace_packet': 'tapeke_hauroki_pākete', 'GATEWAY': '관문기계주소', 'rule': 'ture_uara', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'taurima', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'manuhiri', 'destination': 'ūnga_raraunga_ADDRESS', 'ethernet_port': 'Itarangi_kawe', 'b': 'SECOND_uara', 'MAC': 'mīhini_ADDRESS', 'arp': 'ADDRESS_taumira_pākete', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Porohita_uara', 'port': '접속번호', 'offset': 'OFFSET_uara', 'readable': '읽을수있음', 'c': 'waehere_pūāhua', 'p': 'raraunga_tūranga', 'writers': '쓰기대상들', 'IP': 'Wāhitau_ipurangi_uara', 'e': '보조항목', 'n': 'tuemi_COUNT', 'packet': 'pākete_raraunga', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'whatunga_arawhata', 'window': 'matapihi', 'capture': 'hopu'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
