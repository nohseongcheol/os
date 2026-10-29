#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/Отпрема_Фајлови.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('Отпрема_Фајлови', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Отпрема_Фајлови')
    대응 = {'data': 'подаци', 'i': '순번', 'name': 'Назив', 'c': 'кôд_знака', 'p': 'подаци_позиција', 'args': 'аргумент_низ'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
