#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/코딩시험.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('코딩시험')
    mapovanie_VALUE = {'out': 'KR_údaje', 'expected': '예상결과', 'sdk': 'Development_Kit', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Spustiť_2', 'elf': 'spustiteľný_súbor', 'run': 'Vykonať_príkaz', 'name': 'Názov', 'path': 'Cesta', 'p': 'údaje_pozícia', 'ROOT': 'akcia_koreň', 'report': 'overenie_správa', 'args': 'argument_pole'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
