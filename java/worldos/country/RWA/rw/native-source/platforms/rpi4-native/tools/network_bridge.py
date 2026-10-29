#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/통신다리.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('통신다리', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('통신다리')
    대응 = {'response': '응답자료', 'parts': 'inzira_ikigize', 's': 'igicenteruro_amakurushingiro', 'i': '순번', 'close': 'Gufunga', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'icyinjizwa_agaciro', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'ingingo_ARRAY', 'server': 'seriveri_agaciro', 'data': 'amakurushingiro', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'itegeko_agaciro', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'gucumbikira', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': '커널실행', 'destination': 'aho_ijya_amakurushingiro_aderesi', 'ethernet_port': 'Ethernet_poti', 'b': '둘째값', 'MAC': 'imashini_aderesi', 'arp': 'aderesi_ibonerana_ipaki', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Icyiciro_agaciro', 'port': '접속번호', 'offset': 'Ofuseti_agaciro', 'readable': '읽을수있음', 'c': '문자값', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'Aderesi_ya_Interineti_agaciro', 'e': '보조항목', 'n': '개수', 'packet': 'ipaki_amakurushingiro', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': '통신다리', 'window': 'idirishya', 'capture': 'ishusho_ba7b8054'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
