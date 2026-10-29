#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/épít_PYTHON.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('épít_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('épít_PYTHON')
    leképezés_ÉRTÉK = {'ld': 'kapcsolószerkesztő_eszköz', 'archive': 'archív', 'SHA256': 'ellenőrzés_kivonat', 'build_python': 'készít_PYTHON', 'root': 'gyök_CÍM', 'source': '원본자료', 'name': 'Név', 'path': 'ÚTVONAL', 'VERSION': 'kiadás_ÉRTÉK', 'cc': 'C_fordítóprogram', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'tag'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
