#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/épít_Rendszer.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('épít_Rendszer', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('épít_Rendszer')
    leképezés_ÉRTÉK = {'network': 'hálózat', 'BUILD': 'épít_útvonal', 'ar': 'archív_eszköz', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'betűkészlet_adat', 'flags': 'konfiguráció_BITS', 'a': '첫째값', 'cc': 'C_fordítóprogram', 'args': 'argumentum_TÖMB', 'source_flags': '원본설정', 'ld': 'kapcsolószerkesztő_eszköz', 'method': 'metódus_bejegyzés', 'main': 'Futtatás', 'objcopy': 'objektum_Fájl_átalakító', 'ROOT': 'teendő_gyök', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'fordítóprogram_eszköz', 'build_users': 'készít_felhasználó_tér', 'f': 'Fájl_bejegyzés', 'extra': '추가영역', 'exports': 'exportál_tábla', 'jobs': '빌드작업', 'run': 'végrehajt_parancs', 'path': 'ÚTVONAL', 'REPO': 'adattár_gyök', 'tool': 'Eszközök', 'classes': 'tanóra_útvonal', 'output': 'kimenet', 'samples': '예제들', 'symbol': 'szimbólum_ÉRTÉK', 'source': '원본자료', 'name': 'Név', 'build_network': 'készít_hálózat_48d29d6d', 'font_info': 'betűkészlet_infó', 'manifest': 'köteg_jegyzékfájl', 'work': '작업경로'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
