#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/되돌림시험서버.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('되돌림시험서버')
    대응 = {'data': 'datuak', 'e': '보조항목', 'connection': 'konexio_e05f319b', 'f': 'fitxategi_sarrera', 'peer': 'pareko_balio', 'self': '자신', 'udp': '전문제어', 't': 'Terminal_sarrera', 'tcp': 'konexio_kontrol', 'EchoFixture': '되돌림시험서버', 'args': 'arg_matrize', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
