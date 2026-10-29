#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/되돌림시험서버.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('되돌림시험서버')
    tildeling_VERDI = {'data': 'data', 'e': '보조항목', 'connection': 'kontakt_e05f319b', 'f': 'Fil_oppføring', 'peer': 'node_VERDI_6a3b6fa7', 'self': '자신', 'udp': 'datagram_kontroll', 't': 'Terminal_oppføring', 'tcp': 'kontakt_kontroll', 'EchoFixture': '되돌림시험서버', 'args': 'argument_MATRISE', 'chunk': '조각'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
