#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    mapiranje_VALUE = {'data': 'podaci', 'e': '보조항목', 'connection': 'veza_e05f319b', 'f': 'Datoteka_unos', 'peer': 'ravnopravan_član_VALUE', 'self': '자신', 'udp': 'datogram_kontrola', 't': 'Terminal_unos', 'tcp': 'veza_kontrola', 'EchoFixture': '되돌림시험서버', 'args': 'argument_ARRAY', 'chunk': 'fragment_VALUE'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
