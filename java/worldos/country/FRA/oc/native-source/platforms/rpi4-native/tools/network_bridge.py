#!/usr/bin/env python3
"""기존 CAMIN 호환 진입점. 실제 구현: ../도구/통신다리.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as CAMIN
체계.path.insert(0, str(CAMIN(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('통신다리', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('통신다리')
    대응 = {'response': '응답자료', 'parts': '경로부분', 's': '문자열값', 'i': '순번', 'close': 'Tampar', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': '항목', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': '인수배열', 'server': '서버', 'data': '자료', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': '규칙', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': '호스트', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': '커널실행', 'destination': '목적자료주소', 'ethernet_port': '이더넷접속번호', 'b': '둘째값', 'MAC': '기계주소', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': '순환', 'port': '접속번호', 'offset': '변위', 'readable': '읽을수있음', 'c': '문자값', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': '인터넷주소값', 'e': '보조항목', 'n': '개수', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': '통신다리', 'window': '창', 'capture': '포착여부'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
