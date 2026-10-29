#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/верзија_Мрежа.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('верзија_Мрежа', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('верзија_Мрежа')
    대응 = {'obj': 'одредишна_датотека', 'objects': 'одредиште_Датотеки', 'library': 'библиотека', 'output': '출력결과', 'port': 'број_на_порта', 'root': 'корен_адреса', 'files': 'датотека_Список', 'source': '원본자료', 'run': 'Изврши_наредба', 'flags': 'конфигурација_Услуга_за_интелигентен_пренос_во_заднина', 'path': 'ПАТЕКА', 'build_network': 'Create_Мрежа', 'cc': '시언어번역기', 'ar': 'Архива_алатка'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
