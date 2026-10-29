#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/코딩시험.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('코딩시험')
    toewijzing_WAARDE = {'out': 'HR_gegevens', 'expected': '예상결과', 'sdk': 'Development_Kit', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'starten', 'elf': 'uitvoerbaar_bestand', 'run': 'Uitvoeren_opdracht', 'name': 'Naam', 'path': 'pad', 'p': 'gegevens_functie', 'ROOT': 'Taken_wortel', 'report': 'validatie_Rapport', 'args': 'argument_MATRIX'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
