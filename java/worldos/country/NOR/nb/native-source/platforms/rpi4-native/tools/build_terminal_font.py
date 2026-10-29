#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/bygg_Terminal_skrift.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('bygg_Terminal_skrift', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('bygg_Terminal_skrift')
    tildeling_VERDI = {'data': 'data', 'img': 'tegning_VERDI', 'bits': 'BITS_Liste', 'x': 'x_koordinat', 'draw': 'Tegn_skjermbilde', 'licences': '이용허락목록', 'paths': 'bane_Liste', 'y': 'Y_koordinat', 'main': 'Kjør_2', 'src': '원본주소', 'fonts': 'skrift_Liste', 'ROOT': 'speile_rot', 'p': 'data_plassere', 'cp': 'tegn_koding', 'target': 'mål'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
