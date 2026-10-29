#!/usr/bin/env python3
"""기존 Vojo 호환 진입점. 실제 구현: ../도구/예제되돌림서버.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as Vojo
체계.path.insert(0, str(Vojo(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제되돌림서버')
    대응 = {'data': '자료', 'sock': '소켓', 'tcp_port': '연결접속번호', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': '전문요청처리', 'thread': '작업가닥', 'echo': '되돌림서버항목', 'TCP': '연결요청처리', 'EchoServers': '되돌림서버', 'parser': '인수해석기', 'server': '서버', 'udp_port': '전문접속번호', 'args': '인수배열'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
