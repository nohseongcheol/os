#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/개발꾸러미번역.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('개발꾸러미번역', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('개발꾸러미번역')
    대응 = {'compiler': '번역기', 'obj': 'Zilfichier', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'Laf', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': '인수해석기', 'language': 'Sprooch', 'work': '작업경로', 'args': 'Argument_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
