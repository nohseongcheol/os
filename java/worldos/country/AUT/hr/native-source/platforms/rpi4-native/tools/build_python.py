#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/međuverzija_PYTHON.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('međuverzija_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('međuverzija_PYTHON')
    mapiranje_VALUE = {'ld': '연결편집기', 'archive': 'Arhiva', 'SHA256': 'provjera_raspršivanje', 'build_python': 'Create_PYTHON', 'root': 'korijen_adresa', 'source': '원본자료', 'name': 'Ime', 'path': 'PUTANJA', 'VERSION': 'izdanje_VALUE', 'cc': 'C_kompilator', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'član'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
