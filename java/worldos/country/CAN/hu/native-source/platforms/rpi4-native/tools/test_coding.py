#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/코딩시험.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('코딩시험')
    leképezés_ÉRTÉK = {'out': 'KR_adat', 'expected': '예상결과', 'sdk': 'fejlesztőkészlet', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Futtatás', 'elf': 'végrehajtható_Fájl', 'run': 'végrehajt_parancs', 'name': 'Név', 'path': 'ÚTVONAL', 'p': 'adat_pozíció', 'ROOT': 'teendő_gyök', 'report': 'ellenőrzés_jelent', 'args': 'argumentum_TÖMB'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
