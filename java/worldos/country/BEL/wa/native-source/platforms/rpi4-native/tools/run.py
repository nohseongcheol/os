#!/usr/bin/env python3
"""기존 Tchimin 호환 진입점. 실제 구현: ../도구/실행.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as Tchimin
체계.path.insert(0, str(Tchimin(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('실행', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': '바탕화면실행', 'main': 'Enonder_2', 'host': '호스트', 'status': '상태', 'NetworkBridge': '통신다리', 'ROOT': '기준', 'bridge': '연결다리', 'loader': '적재기', 'base': '바탕', 'options': '선택사항', 'binary': '실행바이너리', 'args': '인수배열', 'command': 'Comande'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
