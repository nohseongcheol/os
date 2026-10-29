#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/test_pc.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('test_pc', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('test_pc')
    toewijzing_WAARDE = {'x': 'x_coördinaat', 'typing': '글자입력', 'message': 'kennisgeving_sms', 'start': 'starten', 'down': '누르는중', 'exact': 'GELIJK_WAARDE', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'symbool', 'j': '안쪽순번', 'deadline': 'deadline_TIJD', 'proc': 'Proces', 'data': 'gegevens', 'main': 'starten', 'w': '너비값', 'init': '초기값', 'block': 'gegevensblok', 'ROOT': 'Taken_wortel', 'text': 'tekst', 'marker': 'markering', 'report': 'validatie_Rapport', 'until': '까지', 'clipboard': 'klembord_WAARDE', 'dst': 'doel_ADRES_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'transcriptie', 'port': 'poortnummer', 'offset': 'VERSCHUIVING_WAARDE', 'h': 'aangevraagd_hoogte_WAARDE', 'src': '원본주소', 'event': 'Gebeurtenis', 'encoding': 'tekenset', 'size': 'Grootte', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_coördinaat', 'output': 'uitvoer', 'symbol': 'symbool_WAARDE', 'client': 'client', 'char': 'tekengegevens', 'rgb': '빛삼원색'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
