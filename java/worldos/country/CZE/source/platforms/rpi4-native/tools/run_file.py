#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/Provést_Soubor.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('Provést_Soubor', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('Provést_Soubor')
    대응 = {'timeout': 'spuštění_TIMEOUT', 's': 'řetězec_data', 'i': '순번', 'match': '일치', 'files': 'seznam_souborů', 'program': 'program', 'executable': 'spustitelný_image', 'args': 'argument_pole', 'chunk': '조각', 'data': 'data', 'proc': 'Proces', 'send': 'poslat', 'main': 'Spustit_2', 'marker': 'značka', 'command': 'příkaz', 'include': 'zahrnout', 'dumped': '갈무리자료', 'run': 'Provést_příkaz', 'p': 'data_pozice', 'parser': 'analyzátor', 'options': 'Možnosti', 'kind': 'oblast_HODNOTA', 'selector': 'selektor', 'upload_data': 'Upload_data', 'end': 'konec_POSUN', 'n': 'zboží_POČET', 'd': 'cíl_data', 'key': '누름값', 'output': 'výstup', 'line': 'vstupní_řádek', 'name': 'Název', 'upload_name': 'Upload_název', 'receive': 'dostat_e_mail'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
