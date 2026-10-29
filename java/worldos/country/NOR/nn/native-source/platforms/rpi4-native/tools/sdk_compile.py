#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/개발꾸러미번역.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('개발꾸러미번역', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('개발꾸러미번역')
    대응 = {'compiler': '번역기', 'obj': 'målfil', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'Køyr_2', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': '인수해석기', 'language': 'Språk', 'work': '작업경로', 'args': 'argument_ARRAY'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
