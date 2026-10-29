#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/되돌림시험서버.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('되돌림시험서버')
    leképezés_ÉRTÉK = {'data': 'adat', 'e': '보조항목', 'connection': 'ismerős_e05f319b', 'f': 'Fájl_bejegyzés', 'peer': 'társ_ÉRTÉK', 'self': '자신', 'udp': 'datagram_vezérlő', 't': 'Terminál_bejegyzés', 'tcp': 'ismerős_vezérlő', 'EchoFixture': '되돌림시험서버', 'args': 'argumentum_TÖMB', 'chunk': '조각'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
