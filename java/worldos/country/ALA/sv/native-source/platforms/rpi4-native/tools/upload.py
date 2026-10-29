#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/Upload_Filer.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('Upload_Filer', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('Upload_Filer')
    mappning_värde = {'data': 'data', 'i': '순번', 'name': 'Namn', 'c': 'kodpunkt', 'p': 'data_placera', 'args': 'argument_MATRIS'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
