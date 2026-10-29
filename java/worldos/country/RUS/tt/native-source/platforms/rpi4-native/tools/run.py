#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/үтәргә_команда.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('үтәргә_команда', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('үтәргә_команда')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'эшләтү_классик', 'main': 'эшләтү', 'host': 'хост', 'status': 'халәт_VALUE', 'NetworkBridge': 'Челтәр_күпер', 'ROOT': 'экранга_җибәрү_тамыр', 'bridge': 'күпер', 'loader': '적재기', 'base': 'Фон_VALUE', 'options': 'Параметрлар', 'binary': 'бинар', 'args': 'аргумент_МАССИВ', 'command': 'команда'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
