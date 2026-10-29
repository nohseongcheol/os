#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/되돌림시험서버.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'подаци', 'e': '보조항목', 'connection': 'веза_e05f319b', 'f': 'фајл_унос', 'peer': 'peer_вриједност', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'веза_контрола', 'EchoFixture': '되돌림시험서버', 'args': 'аргумент_низ', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
