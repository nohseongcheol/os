#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/build_Terminal_skrifttype.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('build_Terminal_skrifttype', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('build_Terminal_skrifttype')
    tilknytning_VÆRDI = {'data': 'data', 'img': 'tegning_VÆRDI', 'bits': 'BITS_Liste', 'x': 'X_koordinat', 'draw': 'tegne_skærmbillede', 'licences': '이용허락목록', 'paths': 'sti_Liste', 'y': 'Y_koordinat', 'main': 'Kør_2', 'src': '원본주소', 'fonts': 'skrifttype_Liste', 'ROOT': 'To_do_rod', 'p': 'data_placere', 'cp': 'tegnkodning', 'target': 'mål'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
