#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/자바라이브러리빌드.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('자바라이브러리빌드')
    대응 = {'header': 'Nadpis_HODNOTA', 'sources': '원문목록', 'i': '순번', 'info': 'Informace_o_systému', 'payload': 'vytížení_data', 'src': '원본주소', 'run': 'Provést_příkaz', 'build_java_library': '자바라이브러리만들기', 'relative': 'relativní_cesta', 'classes': 'Třída_cesta', 'dist': 'distribuce_cesta', 'archive': 'Archiv', 'output': 'výstup', 'root': 'kořen_ODKAZ', 'name': 'Název', 'jar': '자바꾸러미', 'b': 'SEKUNDA_HODNOTA', 'entries': '항목들'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
