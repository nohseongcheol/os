#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/코딩시험.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('코딩시험')
    대응 = {'out': 'мерка_податоци', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Изврши_2', 'elf': '실행파일', 'run': 'Изврши_наредба', 'name': 'Име', 'path': 'ПАТЕКА', 'p': 'податоци_позиционирање', 'ROOT': 'Project_корен', 'report': 'проверка_извештај', 'args': 'аргумент_низа'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
