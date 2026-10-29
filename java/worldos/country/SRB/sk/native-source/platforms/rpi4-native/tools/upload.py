#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/nahrať_Súbory.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('nahrať_Súbory', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('nahrať_Súbory')
    mapovanie_VALUE = {'data': 'údaje', 'i': '순번', 'name': 'Názov', 'c': 'bod_kódu', 'p': 'údaje_pozícia', 'args': 'argument_pole'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
