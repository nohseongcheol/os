#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/BLD_C_kompilátor.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_C_kompilátor', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('BLD_C_kompilátor')
    대응 = {'out': 'KV_data', 'builtins': '내장연산', 'header': 'Nadpis_HODNOTA', 'sdk': 'Development_Kit', 'build_ccompiler': 'Create_C_kompilátor', 'i': '순번', 'elf': 'spustitelný_soubor', 'run': 'Provést_příkaz', 'flags': 'konfigurace_BITS', 'path': 'cesta_2', 'p': 'data_pozice', 'cc': 'C_kompilátor', 'obj': 'cílový_soubor', 'flag': 'Nastavení_HODNOTA', 'ld': 'linker_nástroj', 'objects': 'cíl_Files', 'repo': 'úložiště_cesta', 'v': '임시값', 'upstream': 'upstream', 'root': 'kořen_ODKAZ', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Název', 'includes': '포함인수'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
