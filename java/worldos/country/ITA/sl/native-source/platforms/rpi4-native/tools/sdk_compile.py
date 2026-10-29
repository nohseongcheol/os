#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/komplet_za_razvoj_programske_opreme_prevajati.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('komplet_za_razvoj_programske_opreme_prevajati', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('komplet_za_razvoj_programske_opreme_prevajati')
    preslikava_VALUE = {'compiler': 'prevajalnik_orodje', 'obj': 'ciljna_datoteka', 'sdk': 'razvijalski_komplet', 'output': '출력결과', 'main': 'Zaženi', 'elf': '실행파일', 'is_c': 'informacijska_tehnologija_C_jezik', 'parser': 'razčlenjevalnik', 'language': 'jezik', 'work': '작업경로', 'args': 'argument_ARRAY'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
