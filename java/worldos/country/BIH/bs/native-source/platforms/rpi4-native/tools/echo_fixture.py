#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    대응 = {'data': 'podaci', 'e': '보조항목', 'connection': 'veza_e05f319b', 'f': 'fajl_unos', 'peer': 'peer_VALUE', 'self': '자신', 'udp': '전문제어', 't': 'Terminal_unos', 'tcp': 'veza_kontrola', 'EchoFixture': '되돌림시험서버', 'args': 'argument_niz', 'chunk': '조각'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
