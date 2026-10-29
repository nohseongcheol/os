#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/Upload_Files.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('Upload_Files', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('Upload_Files')
    대응 = {'data': 'data', 'i': '순번', 'name': 'Název', 'c': 'bod_kódu', 'p': 'data_pozice', 'args': 'argument_pole'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
