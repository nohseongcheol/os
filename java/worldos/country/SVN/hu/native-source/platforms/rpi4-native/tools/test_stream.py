#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/teszt_Stream.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('teszt_Stream', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('teszt_Stream')
    leképezés_ÉRTÉK = {'out': 'KR_adat', 'main': 'Futtatás', 'ROOT': 'teendő_gyök', 'p': 'adat_pozíció', 'text': 'Szöveg', 'report': 'ellenőrzés_jelent'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
