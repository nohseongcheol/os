#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/preskusiti_tok.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('preskusiti_tok', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('preskusiti_tok')
    preslikava_VALUE = {'out': 'KR_podatki', 'main': 'Zaženi', 'ROOT': 'pobuda_koren', 'p': 'podatki_položaj', 'text': 'Besedilo', 'report': 'preverjanje_veljavnosti_prijavi'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
