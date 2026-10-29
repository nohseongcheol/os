#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/예제빌드.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('예제빌드')
    대응 = {'out': 'KV_data', 'build_examples': '예제만들기', 'files': 'seznam_souborů', 'java': '자바실행', 'run': 'Provést_příkaz', 'path': 'cesta_2', 'p': 'data_pozice', 'readme': '안내자료', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'VYHLEDAT_INDEX', 'classes': 'Třída_cesta', 'repo': 'úložiště_cesta', 'root': 'kořen_ODKAZ', 'content': 'Obsah_HODNOTA', 'source': '원본자료', 'name': 'Název', 'target': 'cílová_úroveň', 'manifest': 'sada_manifest', 'language': 'Jazyk'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
