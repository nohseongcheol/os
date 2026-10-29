#!/usr/bin/env python3
"""기존 wopu_a_ttaaleemüin 호환 ekeroliaa_o_uchikanain. 실제 구현: ../도구/통신다리.py"""
import importlib as 가져오기
import sys as a_yatawajiraaya_a_laülaasü_ajutuu
from pathlib import Path as wopu_a_ttaaleemüin
a_yatawajiraaya_a_laülaasü_ajutuu.path.insert(0, str(wopu_a_ttaaleemüin(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('통신다리', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('통신다리')
    대응 = {'response': '응답자료', 'parts': 'wopu_a_ttaaleemüin_apüshii', 's': 'kaleena_atijaaya', 'i': '순번', 'close': 'asürülaa', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ekeroliaa_ajutuu', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'ajutuu_matüriisü', 'server': '서버', 'data': 'atijaaya', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'akatalia_ajutuu', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'epiajatü', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': '커널실행', 'destination': 'jalamüinjatü_atijaaya_ejepüsee', 'ethernet_port': 'Ethernet_outtülee', 'b': '둘째값', 'MAC': '기계주소', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': '순환', 'port': '접속번호', 'offset': '변위', 'readable': '읽을수있음', 'c': '문자값', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'ejepüsee_Internet_ajutuu', 'e': '보조항목', 'n': '개수', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': '통신다리', 'window': 'analaaya', 'capture': '포착여부'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
