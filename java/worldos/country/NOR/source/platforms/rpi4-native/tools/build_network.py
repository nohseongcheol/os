#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/bygg_nettverk.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('bygg_nettverk', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('bygg_nettverk')
    tildeling_VERDI = {'obj': 'målfil', 'objects': 'mål_Filer', 'library': 'bibliotek', 'output': 'produksjon', 'port': 'portnummer', 'root': 'rot_e_post', 'files': 'filliste', 'source': '원본자료', 'run': 'Utfør_kommando', 'flags': 'konfigurasjon_BITS', 'path': 'Sti', 'build_network': 'åpne_nettverk', 'cc': 'C_kompilator', 'ar': 'Arkiv_verktøy'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
