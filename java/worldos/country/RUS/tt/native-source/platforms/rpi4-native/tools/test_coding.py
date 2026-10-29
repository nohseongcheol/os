#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/코딩시험.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('코딩시험')
    대응 = {'out': 'үлчәм_мәгълүмат', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'эшләтү', 'elf': '실행파일', 'run': 'үтәргә_команда', 'name': 'исем', 'path': 'Yul', 'p': 'мәгълүмат_урнаштыру', 'ROOT': 'экранга_җибәрү_тамыр', 'report': 'раслау_отчет', 'args': 'аргумент_МАССИВ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
