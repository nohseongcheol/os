#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/Uitvoeren_opdracht.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('Uitvoeren_opdracht', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('Uitvoeren_opdracht')
    toewijzing_WAARDE = {'supported': '지원목록', 'parser': 'parser', 'qemu': '모의기계', 'run_desktop': 'uitvoeren_pc', 'main': 'starten', 'host': 'host', 'status': 'Status_WAARDE', 'NetworkBridge': 'brug_3de4fe3a', 'ROOT': 'Taken_wortel', 'bridge': 'brug', 'loader': 'laadprogramma', 'base': 'Achtergrond_WAARDE', 'options': 'Opties', 'binary': 'binair', 'args': 'argument_MATRIX', 'command': 'opdracht'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
