#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/exportovat_sada_SDK.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('exportovat_sada_SDK', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('exportovat_sada_SDK')
    대응 = {'out': 'KV_data', 'obj': 'cílový_soubor', 'relative': 'relativní_cesta', 'compiler_archive': 'kompilátor_Archiv', 'sdk': 'Development_Kit', 'dist': 'distribuce_cesta', 'archive': 'Archiv', 'main': 'Spustit_2', 'posix': '포직스경로', 'files': 'seznam_souborů', 'source': '원본자료', 'name': 'Název', 'target': 'cílová_úroveň', 'ROOT': 'akce_kořen', 'destination': 'cíl_data_ODKAZ', 'manifest': 'sada_manifest', 'work': '작업경로'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
