#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/build_netværk.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('build_netværk', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('build_netværk')
    tilknytning_VÆRDI = {'obj': 'destinationsfil', 'objects': 'destination_Filer', 'library': 'bibliotek', 'output': 'produktoutput', 'port': 'portnummer', 'root': 'rod_mail', 'files': 'filliste', 'source': '원본자료', 'run': 'Udfør_kommando', 'flags': 'konfiguration_BITS', 'path': 'Sti', 'build_network': 'åbne_netværk', 'cc': 'C_compiler', 'ar': 'Arkiv_værktøj'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
