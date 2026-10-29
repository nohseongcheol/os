#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/exportál_SDK.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('exportál_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('exportál_SDK')
    leképezés_ÉRTÉK = {'out': 'KR_adat', 'obj': 'célfájl', 'relative': 'relatív_elérési_út', 'compiler_archive': 'fordítóprogram_archív', 'sdk': 'fejlesztőkészlet', 'dist': 'elosztás_útvonal', 'archive': 'archív', 'main': 'Futtatás', 'posix': '포직스경로', 'files': 'fájllista', 'source': '원본자료', 'name': 'Név', 'target': 'cél', 'ROOT': 'teendő_gyök', 'destination': 'cél_adat_CÍM', 'manifest': 'köteg_jegyzékfájl', 'work': '작업경로'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
