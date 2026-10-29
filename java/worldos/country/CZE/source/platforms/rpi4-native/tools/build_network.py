#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/BLD_síť.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_síť', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('BLD_síť')
    대응 = {'obj': 'cílový_soubor', 'objects': 'cíl_Files', 'library': 'knihovna', 'output': 'výstup', 'port': 'číslo_portu', 'root': 'kořen_ODKAZ', 'files': 'seznam_souborů', 'source': '원본자료', 'run': 'Provést_příkaz', 'flags': 'konfigurace_BITS', 'path': 'cesta_2', 'build_network': 'Create_síť', 'cc': 'C_kompilátor', 'ar': 'Archiv_nástroj'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
