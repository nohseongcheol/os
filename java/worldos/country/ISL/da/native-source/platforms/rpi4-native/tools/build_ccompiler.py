#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/build_C_compiler.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('build_C_compiler', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('build_C_compiler')
    tilknytning_VÆRDI = {'out': 'KR_data', 'builtins': '내장연산', 'header': 'Header_VÆRDI', 'sdk': 'Development_Kit', 'build_ccompiler': 'åbne_C_compiler', 'i': '순번', 'elf': 'eksekverbar_fil', 'run': 'Udfør_kommando', 'flags': 'konfiguration_BITS', 'path': 'Sti', 'p': 'data_placere', 'cc': 'C_compiler', 'obj': 'destinationsfil', 'flag': 'Indstillinger_VÆRDI', 'ld': 'linker_værktøj', 'objects': 'destination_Filer', 'repo': 'lager_sti', 'v': '임시값', 'upstream': 'upstream', 'root': 'rod_mail', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Navn', 'includes': '포함인수'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
