#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/흐름시험.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('흐름시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('흐름시험')
    대응 = {'out': 'мера_подаци', 'main': 'Покрени', 'ROOT': 'пројектовати_корен', 'p': 'подаци_позиција', 'text': 'Текст', 'report': 'провјера_извештај'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
