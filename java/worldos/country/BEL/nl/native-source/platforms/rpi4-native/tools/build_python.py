#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/build_PYTHON.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('build_PYTHON', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('build_PYTHON')
    toewijzing_WAARDE = {'ld': 'linker_hulpmiddel', 'archive': 'Archief', 'SHA256': 'validatie_hash', 'build_python': 'maken_PYTHON', 'root': 'wortel_ADRES', 'source': '원본자료', 'name': 'Naam', 'path': 'pad', 'VERSION': 'editie_WAARDE', 'cc': 'C_compiler', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'lid'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
