#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/Upload_Files.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('Upload_Files', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('Upload_Files')
    toewijzing_WAARDE = {'data': 'gegevens', 'i': '순번', 'name': 'Naam', 'c': 'codepoint', 'p': 'gegevens_functie', 'args': 'argument_MATRIX'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
