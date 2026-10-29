#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/SDK_qurmaq.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('SDK_qurmaq', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('SDK_qurmaq')
    대응 = {'compiler': '번역기', 'obj': 'təyinat_faylı', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'İcra_Et', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': 'parser', 'language': 'Dil', 'work': '작업경로', 'args': 'arqument_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
