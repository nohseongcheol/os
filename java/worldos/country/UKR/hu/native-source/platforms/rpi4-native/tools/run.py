#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/végrehajt_parancs.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('végrehajt_parancs', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('végrehajt_parancs')
    leképezés_ÉRTÉK = {'supported': '지원목록', 'parser': 'elemző', 'qemu': '모의기계', 'run_desktop': 'futtat_Asztal', 'main': 'Futtatás', 'host': 'gazda', 'status': 'Állapot_ÉRTÉK', 'NetworkBridge': 'híd_3de4fe3a', 'ROOT': 'teendő_gyök', 'bridge': 'híd', 'loader': 'betöltő', 'base': 'Háttér_ÉRTÉK', 'options': 'Beállítások_7f769d16', 'binary': 'bináris', 'args': 'argumentum_TÖMB', 'command': 'Parancs'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
