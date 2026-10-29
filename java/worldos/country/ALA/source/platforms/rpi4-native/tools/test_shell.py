#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/test_Shell.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('test_Shell', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('test_Shell')
    mappning_värde = {'timeout': 'körning_TIMEOUT', 'x': 'x_koordinat', 'msg': 'nätverk_dokument', 'i': '순번', 'reply': 'svara', 'call': '호출', 'args': 'argument_MATRIS', 'chunk': '조각', 'data': 'data', 'proc': 'Process', 'long_text': '긴글', 'restored': '복원자료', 'send': 'skicka', 'file': 'filnamn', 'main': 'Kör', 'found': 'SÖK_KR', 'ROOT': 'åtgärd_rot', 'text': 'text', 'marker': 'markör_8b722c5f', 'command': 'kommando', 'expected': '예상결과', 'pixel': 'bildpunkt', 'shell': 'Shell', 'poll': '준비살피미', 'transcript': 'avskrift', 'end': 'avsluta_FÖRSKJUTNING', 'image': 'BILD', 'key': '누름값', 'y': 'Y_koordinat', 'output': 'utleverans', 'result': 'RESULTAT', 'client': 'klient', 'line': 'inmatningsrad', 'stream': 'flöde_värde', 'name': 'Namn', 'value': 'värde', 'receive': 'få_dokument', 'report': 'validering_Rapport', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
