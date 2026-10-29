#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/Uitvoeren_Bestand.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('Uitvoeren_Bestand', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('Uitvoeren_Bestand')
    toewijzing_WAARDE = {'timeout': 'uitvoerbewerking_TIMEOUT', 's': 'tekenreeks_gegevens', 'i': '순번', 'match': '일치', 'files': 'bestandslijst', 'program': 'app', 'executable': 'uitvoerbaar_kopie', 'args': 'argument_MATRIX', 'chunk': '조각', 'data': 'gegevens', 'proc': 'Proces', 'send': 'e_mailen', 'main': 'starten', 'marker': 'markering', 'command': 'opdracht', 'include': 'bevatten', 'dumped': '갈무리자료', 'run': 'Uitvoeren_opdracht', 'p': 'gegevens_functie', 'parser': 'parser', 'options': 'Opties', 'kind': 'gebied_WAARDE', 'selector': 'selector', 'upload_data': 'Upload_gegevens', 'end': 'beëindigen_VERSCHUIVING', 'n': 'item_AANTAL', 'd': 'doel_gegevens', 'key': '누름값', 'output': 'uitvoer', 'line': 'invoerregel', 'name': 'Naam', 'upload_name': 'Upload_naam', 'receive': 'ontvangen_e_mail'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
