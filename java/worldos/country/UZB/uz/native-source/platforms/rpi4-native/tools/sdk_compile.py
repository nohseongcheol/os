#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/개발꾸러미번역.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('개발꾸러미번역', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('개발꾸러미번역')
    대응 = {'compiler': '번역기', 'obj': 'natijalar_fayli', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'Bajarish', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': 'parser', 'language': 'Til', 'work': '작업경로', 'args': 'dalil_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
