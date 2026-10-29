#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    대응 = {'data': 'të_dhëna', 'e': '보조항목', 'connection': 'lidhje_e05f319b', 'f': 'skedar_futje', 'peer': 'homolog_VALUE', 'self': '자신', 'udp': '전문제어', 't': 'Terminali_futje', 'tcp': 'lidhje_kontroll', 'EchoFixture': '되돌림시험서버', 'args': 'argument_ARRAY', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
