#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    대응 = {'data': 'податоци', 'e': '보조항목', 'connection': 'врска_e05f319b', 'f': 'датотека_внес', 'peer': 'рамноправен_уред_VALUE', 'self': '자신', 'udp': '전문제어', 't': 'Терминал_внес', 'tcp': 'врска_контрола', 'EchoFixture': '되돌림시험서버', 'args': 'аргумент_низа', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
