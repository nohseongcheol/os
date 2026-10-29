#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/코딩시험.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('코딩시험')
    대응 = {'out': 'KV_data', 'expected': '예상결과', 'sdk': 'Development_Kit', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Spustit_2', 'elf': 'spustitelný_soubor', 'run': 'Provést_příkaz', 'name': 'Název', 'path': 'cesta_2', 'p': 'data_pozice', 'ROOT': 'akce_kořen', 'report': 'ověření_Zpráva', 'args': 'argument_pole'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
