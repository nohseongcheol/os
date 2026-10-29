#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    mapiranje_VALUE = {'data': 'podaci', 'e': '보조항목', 'connection': 'veza_e05f319b', 'f': 'Datoteka_stavka', 'peer': 'ravnopravni_uređaj_VALUE', 'self': '자신', 'udp': 'datagram_kontrola', 't': 'Terminal_stavka', 'tcp': 'veza_kontrola', 'EchoFixture': '되돌림시험서버', 'args': 'argument_niz', 'chunk': '조각'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
