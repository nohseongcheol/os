#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/통신다리.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('통신다리', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('통신다리')
    대응 = {'response': '응답자료', 'parts': 'ýol_komponent', 's': 'setir_maglumat', 'i': '순번', 'close': 'Ýap', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'girizmeklik_baha', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'argument_ARRAY', 'server': 'serwer_baha', 'data': 'maglumat', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'kada_baha', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'esasy', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': '커널실행', 'destination': 'barylmaly_ýer_maglumat_salgy', 'ethernet_port': 'Ethernet_port', 'b': '둘째값', 'MAC': 'kompýuter_salgy', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Gaýtalanyş_baha', 'port': '접속번호', 'offset': 'Süýşüriş_baha', 'readable': '읽을수있음', 'c': 'nyşanyň_kody', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'Internet_salgy_baha', 'e': '보조항목', 'n': '개수', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': '통신다리', 'window': 'penjire', 'capture': 'düşüriş'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
