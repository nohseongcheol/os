#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/실행파일시험.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('실행파일시험')
    대응 = {'out': 'KV_data', 'expected': '예상결과', 'phoff': 'program_Nadpis_POSUN', 'offset': 'POSUN_HODNOTA', 'invalid': 'neplatný_data', 'path': 'cesta_2', 'executable': 'spustitelný_image', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'VÝSLEDEK', 'format_': 'formát_b87fd068', 'main': 'Spustit_2', 'content': 'Obsah_HODNOTA', 'source': '원본자료', 'name': 'Název', 'reference': 'Porovnání_účaří', 'ROOT': 'akce_kořen', 'value': 'HODNOTA', 'report': 'ověření_Zpráva'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
