#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/épít_hálózat.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('épít_hálózat', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('épít_hálózat')
    leképezés_ÉRTÉK = {'obj': 'célfájl', 'objects': 'cél_Files', 'library': 'kódtár', 'output': 'kimenet', 'port': 'portszám', 'root': 'gyök_CÍM', 'files': 'fájllista', 'source': '원본자료', 'run': 'végrehajt_parancs', 'flags': 'konfiguráció_BITS', 'path': 'ÚTVONAL', 'build_network': 'készít_hálózat_48d29d6d', 'cc': 'C_fordítóprogram', 'ar': 'archív_eszköz'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
