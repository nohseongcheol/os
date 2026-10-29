#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/자바라이브러리빌드.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('자바라이브러리빌드')
    tilknytning_VÆRDI = {'header': 'Header_VÆRDI', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'nyttedata_data', 'src': '원본주소', 'run': 'Udfør_kommando', 'build_java_library': '자바라이브러리만들기', 'relative': 'relativ_sti', 'classes': 'Hold_sti', 'dist': 'distribution_sti', 'archive': 'Arkiv', 'output': 'produktoutput', 'root': 'rod_mail', 'name': 'Navn', 'jar': '자바꾸러미', 'b': 'SEKUND_VÆRDI', 'entries': '항목들'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
