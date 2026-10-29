#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    대응 = {'data': 'data', 'e': '보조항목', 'connection': 'kontakt_e05f319b', 'f': 'fil_oppføring', 'peer': 'node_VALUE_6a3b6fa7', 'self': '자신', 'udp': '전문제어', 't': 'Terminal_oppføring', 'tcp': 'kontakt_styring', 'EchoFixture': '되돌림시험서버', 'args': 'argument_ARRAY', 'chunk': '조각'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
