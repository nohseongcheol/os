#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/épít_C_fordítóprogram.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('épít_C_fordítóprogram', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('épít_C_fordítóprogram')
    leképezés_ÉRTÉK = {'out': 'KR_adat', 'builtins': '내장연산', 'header': 'fejléc_ÉRTÉK', 'sdk': 'fejlesztőkészlet', 'build_ccompiler': 'készít_C_fordítóprogram', 'i': '순번', 'elf': 'végrehajtható_Fájl', 'run': 'végrehajt_parancs', 'flags': 'konfiguráció_BITS', 'path': 'ÚTVONAL', 'p': 'adat_pozíció', 'cc': 'C_fordítóprogram', 'obj': 'célfájl', 'flag': 'Gépház_ÉRTÉK', 'ld': 'kapcsolószerkesztő_eszköz', 'objects': 'cél_Files', 'repo': 'adattár_útvonal', 'v': '임시값', 'upstream': 'kiinduló', 'root': 'gyök_CÍM', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Név', 'includes': '포함인수'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
