#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/graditev_PYTHON.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('graditev_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('graditev_PYTHON')
    preslikava_VALUE = {'ld': '연결편집기', 'archive': 'Arhiv', 'SHA256': 'preverjanje_veljavnosti_zgoščena_vrednost', 'build_python': 'Ustvari_PYTHON', 'root': 'koren_naslov', 'source': '원본자료', 'name': 'Ime', 'path': 'POT', 'VERSION': 'izdaja_VALUE', 'cc': 'C_prevajalnik', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'član'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
