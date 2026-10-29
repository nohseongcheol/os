#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/되돌림시험서버.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('되돌림시험서버')
    mappning_värde = {'data': 'data', 'e': '보조항목', 'connection': 'kontakt_e05f319b', 'f': 'fil_post', 'peer': 'peer_värde', 'self': '자신', 'udp': 'datagram_kontroll', 't': 'Terminal_post', 'tcp': 'kontakt_kontroll', 'EchoFixture': '되돌림시험서버', 'args': 'argument_MATRIS', 'chunk': '조각'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
