#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/build_C_compiler.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('build_C_compiler', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('build_C_compiler')
    toewijzing_WAARDE = {'out': 'HR_gegevens', 'builtins': '내장연산', 'header': 'header_WAARDE', 'sdk': 'Development_Kit', 'build_ccompiler': 'maken_C_compiler', 'i': '순번', 'elf': 'uitvoerbaar_bestand', 'run': 'Uitvoeren_opdracht', 'flags': 'configuratie_BITS', 'path': 'pad', 'p': 'gegevens_functie', 'cc': 'C_compiler', 'obj': 'doelbestand', 'flag': 'Instellingen_WAARDE', 'ld': 'linker_hulpmiddel', 'objects': 'doel_Files', 'repo': 'opslagplaats_pad', 'v': '임시값', 'upstream': 'upstream', 'root': 'wortel_ADRES', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Naam', 'includes': '포함인수'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
