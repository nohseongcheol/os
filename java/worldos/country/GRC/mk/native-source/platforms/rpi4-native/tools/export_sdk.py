#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/извези_SDK.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('извези_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('извези_SDK')
    대응 = {'out': 'мерка_податоци', 'obj': 'одредишна_датотека', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'Архива', 'main': 'Изврши_2', 'posix': '포직스경로', 'files': 'датотека_Список', 'source': '원본자료', 'name': 'Име', 'target': 'цел', 'ROOT': 'Project_корен', 'destination': 'одредиште_податоци_адреса', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
