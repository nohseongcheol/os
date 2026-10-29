#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/sada_SDK_kompilovat.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('sada_SDK_kompilovat', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('sada_SDK_kompilovat')
    대응 = {'compiler': 'kompilátor_nástroj', 'obj': 'cílový_soubor', 'sdk': 'Development_Kit', 'output': 'výstup', 'main': 'Spustit_2', 'elf': 'spustitelný_soubor', 'is_c': 'informační_systémy_C_Jazyk', 'parser': 'analyzátor', 'language': 'Jazyk', 'work': '작업경로', 'args': 'argument_pole'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
