#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/Izvedi_ukaz.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('Izvedi_ukaz', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Izvedi_ukaz')
    preslikava_VALUE = {'supported': '지원목록', 'parser': 'razčlenjevalnik', 'qemu': '모의기계', 'run_desktop': 'izvajati_namizje', 'main': 'Zaženi', 'host': 'gostiti', 'status': 'stanje_VALUE', 'NetworkBridge': 'most_3de4fe3a', 'ROOT': 'pobuda_koren', 'bridge': 'most', 'loader': 'nalagalnik', 'base': 'Ozadje_VALUE', 'options': 'Možnosti', 'binary': 'binary', 'args': 'argument_ARRAY', 'command': 'Ukaz'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
