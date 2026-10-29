#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/zostava_sieť.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('zostava_sieť', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('zostava_sieť')
    mapovanie_VALUE = {'obj': 'cieľový_súbor', 'objects': 'cieľ_Súbory', 'library': 'knižnica', 'output': '출력결과', 'port': 'číslo_portu', 'root': 'koreň_adresa', 'files': 'Súbor_Zoznam', 'source': '원본자료', 'run': 'Vykonať_príkaz', 'flags': 'konfigurácia_Background_Intelligent_Transfer_Service', 'path': 'Cesta', 'build_network': 'Create_sieť', 'cc': 'C_kompilátor', 'ar': 'Archív_nástroj'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
