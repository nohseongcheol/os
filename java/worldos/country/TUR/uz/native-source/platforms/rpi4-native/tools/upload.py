#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/uzatmoq_Fayllar.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('uzatmoq_Fayllar', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('uzatmoq_Fayllar')
    대응 = {'data': 'ma_lumotlar', 'i': '순번', 'name': 'Nomi', 'c': 'belgi_kodi', 'p': 'ma_lumotlar_holat', 'args': 'dalil_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
