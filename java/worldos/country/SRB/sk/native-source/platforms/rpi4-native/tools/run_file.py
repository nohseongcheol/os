#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/Vykonať_Súbor.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('Vykonať_Súbor', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Vykonať_Súbor')
    mapovanie_VALUE = {'timeout': '시간제한', 's': 'reťazec_údaje', 'i': '순번', 'match': '일치', 'files': 'Súbor_Zoznam', 'program': 'program', 'executable': 'spustiteľný_súbor_IMAGE', 'args': 'argument_pole', 'chunk': '조각', 'data': 'údaje', 'proc': 'Proces', 'send': 'odoslať', 'main': 'Spustiť_2', 'marker': 'fixka', 'command': 'Príkaz', 'include': 'zahrnúť', 'dumped': '갈무리자료', 'run': 'Vykonať_príkaz', 'p': 'údaje_pozícia', 'parser': 'analyzátor', 'options': 'Možnosti', 'kind': 'oblasť_VALUE', 'selector': 'selektor', 'upload_data': 'nahrať_údaje', 'end': 'ukončiť_hovor_Posun', 'n': 'položka_COUNT', 'd': 'cieľ_údaje', 'key': '누름값', 'output': '출력결과', 'line': 'riadok', 'name': 'Názov', 'upload_name': 'nahrať_názov', 'receive': 'dostať_e_mail'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
