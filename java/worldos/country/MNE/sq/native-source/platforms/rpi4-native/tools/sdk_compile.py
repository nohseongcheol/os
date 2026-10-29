#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/개발꾸러미번역.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('개발꾸러미번역', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('개발꾸러미번역')
    대응 = {'compiler': '번역기', 'obj': 'skedari_i_vendmbërritjes', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'Ekzekuto', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': 'analizues', 'language': 'Gjuha', 'work': '작업경로', 'args': 'argument_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
