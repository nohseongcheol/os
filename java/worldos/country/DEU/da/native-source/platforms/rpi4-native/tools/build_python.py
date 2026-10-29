#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/build_PYTHON.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('build_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('build_PYTHON')
    tilknytning_VÆRDI = {'ld': 'linker_værktøj', 'archive': 'Arkiv', 'SHA256': 'validering_hash', 'build_python': 'åbne_PYTHON', 'root': 'rod_mail', 'source': '원본자료', 'name': 'Navn', 'path': 'Sti', 'VERSION': '배포판', 'cc': 'C_compiler', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'medlem'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
