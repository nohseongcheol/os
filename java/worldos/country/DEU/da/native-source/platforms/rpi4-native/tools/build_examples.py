#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/예제빌드.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('예제빌드')
    tilknytning_VÆRDI = {'out': 'KR_data', 'build_examples': '예제만들기', 'files': 'filliste', 'java': '자바실행', 'run': 'Udfør_kommando', 'path': 'Sti', 'p': 'data_placere', 'readme': 'Vigtigt', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'Opslag_INDEKS', 'classes': 'Hold_sti', 'repo': 'lager_sti', 'root': 'rod_mail', 'content': 'Indhold_VÆRDI', 'source': '원본자료', 'name': 'Navn', 'target': 'mål', 'manifest': 'bundt_manifest', 'language': 'Sprog'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
