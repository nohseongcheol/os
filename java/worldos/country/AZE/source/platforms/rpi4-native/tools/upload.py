#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/Upload_Fayllar.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('Upload_Fayllar', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Upload_Fayllar')
    대응 = {'data': 'verilənlər', 'i': '순번', 'name': 'Ad', 'c': 'simvol_kodu', 'p': 'verilənlər_yerinə_qoymaq', 'args': 'arqument_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
