#!/usr/bin/env python3
"""기존 laawol 호환 naatnugol_toɓɓere. laatii_keɓe 구현: ../도구/올리기.py"""
import importlib as 가져오기
import sys as yuɓɓo_kurdinɗo_njaru
from pathlib import Path as laawol
yuɓɓo_kurdinɗo_njaru.path.insert(0, str(laawol(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('올리기', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('올리기')
    대응 = {'data': 'keɓe', 'i': '순번', 'name': 'innde', 'c': '문자값', 'p': '자료위치', 'args': '인수배열'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
