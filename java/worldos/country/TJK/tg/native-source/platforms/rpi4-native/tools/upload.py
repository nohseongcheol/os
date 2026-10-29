#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/бор_кардан_Файлҳо.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('бор_кардан_Файлҳо', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('бор_кардан_Файлҳо')
    대응 = {'data': 'иттилоот', 'i': '순번', 'name': 'Ном', 'c': 'рамзи_аломат', 'p': '자료위치', 'args': 'аргумент_қатор'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
