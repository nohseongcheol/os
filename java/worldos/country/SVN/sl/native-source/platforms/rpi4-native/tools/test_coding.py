#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/코딩시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('코딩시험')
    preslikava_VALUE = {'out': 'KR_podatki', 'expected': '예상결과', 'sdk': 'razvijalski_komplet', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Zaženi', 'elf': '실행파일', 'run': 'Izvedi_ukaz', 'name': 'Ime', 'path': 'POT', 'p': 'podatki_položaj', 'ROOT': 'pobuda_koren', 'report': 'preverjanje_veljavnosti_prijavi', 'args': 'argument_ARRAY'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
