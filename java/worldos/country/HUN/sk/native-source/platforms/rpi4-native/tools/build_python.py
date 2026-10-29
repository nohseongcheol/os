#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/zostava_PYTHON.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('zostava_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('zostava_PYTHON')
    mapovanie_VALUE = {'ld': '연결편집기', 'archive': 'Archív', 'SHA256': 'overenie_hodnota_hash', 'build_python': 'Create_PYTHON', 'root': 'koreň_adresa', 'source': '원본자료', 'name': 'Názov', 'path': 'Cesta', 'VERSION': 'vydanie_VALUE', 'cc': 'C_kompilátor', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'člen'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
