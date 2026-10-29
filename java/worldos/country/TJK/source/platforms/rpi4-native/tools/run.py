#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/иҷро_кардан_фармон.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('иҷро_кардан_фармон', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('иҷро_кардан_фармон')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'порча_мизи_корӣ', 'main': 'порча', 'host': 'мизбон', 'status': 'вазъият_қимат', 'NetworkBridge': 'Шабака_кӯпрук', 'ROOT': '기준', 'bridge': 'кӯпрук', 'loader': '적재기', 'base': 'Пасзамина_қимат', 'options': 'Имконот', 'binary': 'дуӣ', 'args': 'аргумент_қатор', 'command': 'фармон'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
