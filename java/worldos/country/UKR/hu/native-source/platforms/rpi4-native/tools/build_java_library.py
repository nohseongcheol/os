#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/자바라이브러리빌드.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('자바라이브러리빌드')
    leképezés_ÉRTÉK = {'header': 'fejléc_ÉRTÉK', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'teher_adat', 'src': '원본주소', 'run': 'végrehajt_parancs', 'build_java_library': '자바라이브러리만들기', 'relative': 'relatív_elérési_út', 'classes': 'tanóra_útvonal', 'dist': 'elosztás_útvonal', 'archive': 'archív', 'output': 'kimenet', 'root': 'gyök_CÍM', 'name': 'Név', 'jar': '자바꾸러미', 'b': 'MPERC_ÉRTÉK', 'entries': '항목들'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
