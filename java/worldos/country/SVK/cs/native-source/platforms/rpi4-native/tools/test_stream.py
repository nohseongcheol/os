#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/test_tok.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_tok', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('test_tok')
    대응 = {'out': 'KV_data', 'main': 'Spustit_2', 'ROOT': 'akce_kořen', 'p': 'data_pozice', 'text': 'text', 'report': 'ověření_Zpráva'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
