#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/실행파일시험.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('실행파일시험')
    mappning_värde = {'out': 'KR_data', 'expected': '예상결과', 'phoff': 'app_huvud_FÖRSKJUTNING', 'offset': 'FÖRSKJUTNING_värde', 'invalid': 'ogiltig_data', 'path': 'sökväg_2', 'executable': 'körbar_fil_BILD', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'RESULTAT', 'format_': 'format_b87fd068', 'main': 'Kör', 'content': 'Innehåll_värde', 'source': '원본자료', 'name': 'Namn', 'reference': 'Jämförelse_baslinje', 'ROOT': 'åtgärd_rot', 'value': 'värde', 'report': 'validering_Rapport'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
