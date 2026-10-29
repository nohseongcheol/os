#!/usr/bin/env python3
"""기존 འགྲུལ_ལམ 호환 진입점. 실제 구현: ../도구/되돌림시험서버.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as འགྲུལ_ལམ
체계.path.insert(0, str(འགྲུལ_ལམ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': '자료', 'e': '보조항목', 'connection': '접속', 'f': '파일항목', 'peer': '상대', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': '연결제어', 'EchoFixture': '되돌림시험서버', 'args': '인수배열', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
