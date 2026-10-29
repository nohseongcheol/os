#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/BLD_PYTHON.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_PYTHON', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('BLD_PYTHON')
    대응 = {'ld': 'linker_nástroj', 'archive': 'Archiv', 'SHA256': 'ověření_hodnota_hash', 'build_python': 'Create_PYTHON', 'root': 'kořen_ODKAZ', 'source': '원본자료', 'name': 'Název', 'path': 'cesta_2', 'VERSION': 'edice_HODNOTA', 'cc': 'C_kompilátor', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'člen'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
