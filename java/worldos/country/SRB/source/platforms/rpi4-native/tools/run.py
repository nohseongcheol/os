#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/Изврши_команда.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('Изврши_команда', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Изврши_команда')
    대응 = {'supported': '지원목록', 'parser': 'анализатор', 'qemu': '모의기계', 'run_desktop': 'низ_десктоп', 'main': 'Покрени', 'host': 'хост', 'status': 'стање_вриједност', 'NetworkBridge': 'Мрежа_мост', 'ROOT': 'пројектовати_корен', 'bridge': 'мост', 'loader': '적재기', 'base': 'постер_вриједност', 'options': 'Опције', 'binary': 'бинарно', 'args': 'аргумент_низ', 'command': 'Наредба'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
