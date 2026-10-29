#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/실행파일시험.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('실행파일시험')
    toewijzing_WAARDE = {'out': 'HR_gegevens', 'expected': '예상결과', 'phoff': 'app_header_VERSCHUIVING', 'offset': 'VERSCHUIVING_WAARDE', 'invalid': 'nietig_gegevens', 'path': 'pad', 'executable': 'uitvoerbaar_kopie', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'resultaat', 'format_': 'opmaak_b87fd068', 'main': 'starten', 'content': 'Inhoud_WAARDE', 'source': '원본자료', 'name': 'Naam', 'reference': 'Vergelijking_basislijn', 'ROOT': 'Taken_wortel', 'value': 'WAARDE', 'report': 'validatie_Rapport'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
