#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/köra_kommando.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('köra_kommando', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('köra_kommando')
    mappning_värde = {'supported': '지원목록', 'parser': 'parser', 'qemu': '모의기계', 'run_desktop': 'köra_Dator', 'main': 'Kör', 'host': 'värd', 'status': 'status_värde', 'NetworkBridge': 'brygga_3de4fe3a', 'ROOT': 'åtgärd_rot', 'bridge': 'brygga', 'loader': 'inläsare', 'base': 'Bakgrund_värde', 'options': 'Alternativ', 'binary': 'binär', 'args': 'argument_MATRIS', 'command': 'kommando'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
