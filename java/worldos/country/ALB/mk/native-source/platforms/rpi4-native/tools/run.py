#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/Изврши_наредба.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('Изврши_наредба', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Изврши_наредба')
    대응 = {'supported': '지원목록', 'parser': 'анализатор', 'qemu': '모의기계', 'run_desktop': 'изврши_десктоп', 'main': 'Изврши_2', 'host': 'вдоми', 'status': 'статус_VALUE', 'NetworkBridge': 'Мрежа_мост', 'ROOT': 'Project_корен', 'bridge': 'мост', 'loader': '적재기', 'base': 'тапет_VALUE', 'options': 'Опции', 'binary': 'бинарен', 'args': 'аргумент_низа', 'command': 'Команда'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
