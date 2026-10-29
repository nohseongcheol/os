#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/SDK_изгради.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('SDK_изгради', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('SDK_изгради')
    대응 = {'compiler': '번역기', 'obj': 'одредишна_датотека', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'Изврши_2', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': 'анализатор', 'language': 'јазик', 'work': '작업경로', 'args': 'аргумент_низа'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
