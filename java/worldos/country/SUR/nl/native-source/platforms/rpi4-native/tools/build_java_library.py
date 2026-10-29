#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/자바라이브러리빌드.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('자바라이브러리빌드')
    toewijzing_WAARDE = {'header': 'header_WAARDE', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'payload_gegevens', 'src': '원본주소', 'run': 'Uitvoeren_opdracht', 'build_java_library': '자바라이브러리만들기', 'relative': 'relatief_pad', 'classes': 'les_pad', 'dist': 'distributie_pad', 'archive': 'Archief', 'output': 'uitvoer', 'root': 'wortel_ADRES', 'name': 'Naam', 'jar': '자바꾸러미', 'b': 'SECONDE_WAARDE', 'entries': '항목들'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
