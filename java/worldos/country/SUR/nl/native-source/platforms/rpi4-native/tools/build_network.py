#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/build_net.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('build_net', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('build_net')
    toewijzing_WAARDE = {'obj': 'doelbestand', 'objects': 'doel_Files', 'library': 'bibliotheek', 'output': 'uitvoer', 'port': 'poortnummer', 'root': 'wortel_ADRES', 'files': 'bestandslijst', 'source': '원본자료', 'run': 'Uitvoeren_opdracht', 'flags': 'configuratie_BITS', 'path': 'pad', 'build_network': 'maken_net', 'cc': 'C_compiler', 'ar': 'Archief_hulpmiddel'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
