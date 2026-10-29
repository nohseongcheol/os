#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/exporteren_SDK.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('exporteren_SDK', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('exporteren_SDK')
    toewijzing_WAARDE = {'out': 'HR_gegevens', 'obj': 'doelbestand', 'relative': 'relatief_pad', 'compiler_archive': 'compiler_Archief', 'sdk': 'Development_Kit', 'dist': 'distributie_pad', 'archive': 'Archief', 'main': 'starten', 'posix': '포직스경로', 'files': 'bestandslijst', 'source': '원본자료', 'name': 'Naam', 'target': 'doel', 'ROOT': 'Taken_wortel', 'destination': 'doel_gegevens_ADRES', 'manifest': 'bundel_manifest', 'work': '작업경로'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
