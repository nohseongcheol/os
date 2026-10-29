#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/되돌림시험서버.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'иттилоот', 'e': '보조항목', 'connection': 'пайваст_e05f319b', 'f': 'файл_ворида', 'peer': 'ҳамсон_қимат', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'пайваст_идоракунӣ', 'EchoFixture': '되돌림시험서버', 'args': 'аргумент_қатор', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
