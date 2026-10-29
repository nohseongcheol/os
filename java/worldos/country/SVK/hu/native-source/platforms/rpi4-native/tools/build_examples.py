#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/예제빌드.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('예제빌드')
    leképezés_ÉRTÉK = {'out': 'KR_adat', 'build_examples': '예제만들기', 'files': 'fájllista', 'java': '자바실행', 'run': 'végrehajt_parancs', 'path': 'ÚTVONAL', 'p': 'adat_pozíció', 'readme': 'fontos_fájl', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'KERES_INDEX', 'classes': 'tanóra_útvonal', 'repo': 'adattár_útvonal', 'root': 'gyök_CÍM', 'content': 'Tartalom_ÉRTÉK', 'source': '원본자료', 'name': 'Név', 'target': 'cél', 'manifest': 'köteg_jegyzékfájl', 'language': 'Nyelv'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
