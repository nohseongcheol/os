#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/version_Terminal_teckensnitt.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('version_Terminal_teckensnitt', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('version_Terminal_teckensnitt')
    mappning_värde = {'data': 'data', 'img': 'ritning_värde', 'bits': 'BITS_ange', 'x': 'x_koordinat', 'draw': 'Rita_skärmbild', 'licences': '이용허락목록', 'paths': 'väg_ange', 'y': 'Y_koordinat', 'main': 'Kör', 'src': '원본주소', 'fonts': 'teckensnitt_ange', 'ROOT': 'åtgärd_rot', 'p': 'data_placera', 'cp': 'teckenkodning', 'target': 'mål'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
