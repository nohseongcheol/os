#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/verzija_PYTHON.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('verzija_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('verzija_PYTHON')
    mapiranje_VALUE = {'ld': '연결편집기', 'archive': 'Arhiva', 'SHA256': 'provera_valjanosti_heš', 'build_python': 'Create_PYTHON', 'root': 'koren_adresa', 'source': '원본자료', 'name': 'ime', 'path': 'putanja', 'VERSION': 'izdanje_VALUE', 'cc': 'C_kompajler', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'član'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
