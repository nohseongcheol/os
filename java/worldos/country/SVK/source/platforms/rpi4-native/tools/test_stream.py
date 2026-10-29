#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/test_Stream.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('test_Stream', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('test_Stream')
    mapovanie_VALUE = {'out': 'KR_údaje', 'main': 'Spustiť_2', 'ROOT': 'akcia_koreň', 'p': 'údaje_pozícia', 'text': 'Spracovanie_textu', 'report': 'overenie_správa'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
