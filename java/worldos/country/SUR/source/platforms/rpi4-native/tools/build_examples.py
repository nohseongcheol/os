#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/예제빌드.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('예제빌드')
    toewijzing_WAARDE = {'out': 'HR_gegevens', 'build_examples': '예제만들기', 'files': 'bestandslijst', 'java': '자바실행', 'run': 'Uitvoeren_opdracht', 'path': 'pad', 'p': 'gegevens_functie', 'readme': 'LEESMIJ', 'build_java_library': '자바라이브러리만들기', 'code': 'instructie_REEKS', 'index': 'ZOEKEN_INDEX', 'classes': 'les_pad', 'repo': 'opslagplaats_pad', 'root': 'wortel_ADRES', 'content': 'Inhoud_WAARDE', 'source': '원본자료', 'name': 'Naam', 'target': 'doel', 'manifest': 'bundel_manifest', 'language': 'Taal'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
