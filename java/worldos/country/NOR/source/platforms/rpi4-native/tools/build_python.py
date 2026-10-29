#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/bygg_PYTHON.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('bygg_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('bygg_PYTHON')
    tildeling_VERDI = {'ld': 'koblingsprogram_verktøy', 'archive': 'Arkiv', 'SHA256': 'validering_hash', 'build_python': 'åpne_PYTHON', 'root': 'rot_e_post', 'source': '원본자료', 'name': 'Navn', 'path': 'Sti', 'VERSION': 'utgave_Edition_VERDI', 'cc': 'C_kompilator', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'medlem'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
