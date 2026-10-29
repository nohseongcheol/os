#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/épít_Terminál_betűkészlet.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('épít_Terminál_betűkészlet', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('épít_Terminál_betűkészlet')
    leképezés_ÉRTÉK = {'data': 'adat', 'img': 'rajz_ÉRTÉK', 'bits': 'BITS_Lista', 'x': 'x_koordináta', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'útvonal_Lista', 'y': 'Y_koordináta', 'main': 'Futtatás', 'src': '원본주소', 'fonts': 'betűkészlet_Lista', 'ROOT': 'teendő_gyök', 'p': 'adat_pozíció', 'cp': 'karakterkódolás', 'target': 'cél'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
