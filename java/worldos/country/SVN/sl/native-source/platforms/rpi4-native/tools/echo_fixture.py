#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    preslikava_VALUE = {'data': 'podatki', 'e': '보조항목', 'connection': 'povezava_e05f319b', 'f': 'Datoteka_vnos', 'peer': 'enakovreden_VALUE', 'self': '자신', 'udp': 'datagram_nadzor', 't': 'Terminal_vnos', 'tcp': 'povezava_nadzor', 'EchoFixture': '되돌림시험서버', 'args': 'argument_ARRAY', 'chunk': '조각'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
