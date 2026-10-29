#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/test_Shell.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('test_Shell', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('test_Shell')
    toewijzing_WAARDE = {'timeout': 'uitvoerbewerking_TIMEOUT', 'x': 'x_coördinaat', 'msg': 'net_e_mail', 'i': '순번', 'reply': 'reactie', 'call': '호출', 'args': 'argument_MATRIX', 'chunk': '조각', 'data': 'gegevens', 'proc': 'Proces', 'long_text': '긴글', 'restored': '복원자료', 'send': 'e_mailen', 'file': 'bestand', 'main': 'starten', 'found': 'Search_HR', 'ROOT': 'Taken_wortel', 'text': 'tekst', 'marker': 'markering', 'command': 'opdracht', 'expected': '예상결과', 'pixel': 'pixel', 'shell': 'Shell', 'poll': '준비살피미', 'transcript': 'transcriptie', 'end': 'beëindigen_VERSCHUIVING', 'image': 'kopie', 'key': '누름값', 'y': 'Y_coördinaat', 'output': 'uitvoer', 'result': 'resultaat', 'client': 'client', 'line': 'invoerregel', 'stream': 'Stream_WAARDE', 'name': 'Naam', 'value': 'WAARDE', 'receive': 'ontvangen_e_mail', 'report': 'validatie_Rapport', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
