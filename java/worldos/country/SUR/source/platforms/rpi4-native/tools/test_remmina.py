#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/원격한글시험.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('원격한글시험')
    toewijzing_WAARDE = {'wait': '기다리기', 'typing': '글자입력', 'start': 'starten', 'profile': 'Profiel', 'focused': 'Prioriteit', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_WAARDE', 'log': 'LOG_RECORD', 'args': 'argument_MATRIX', 'deadline': 'deadline_TIJD', 'data': 'gegevens', 'candidate': 'sollicitant', 'logs': '기록들', 'kw': 'benoemd_argument', 'number': '수치', 'main': 'starten', 'ready': '준비완료', 'found': 'Search_HR', 'guest': 'gast', 'ROOT': 'Taken_wortel', 'marker': 'markering', 'text': 'tekst', 'out': 'HR_gegevens', 'env': 'omgeving', 'f': 'Bestand_invoer', 'port': 'poortnummer', 'offset': 'VERSCHUIVING_WAARDE', 'version': 'versienummer', 'p': 'gegevens_functie', 'selector': 'selector', 'xvfb': 'virtueel_weergeven', 'display': 'beeldscherm', 'n': 'item_AANTAL', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': 'virtueel_invoer_hulpmiddel', 'name': 'Naam', 'window': 'Venster', 'report': 'validatie_Rapport', 'work': '작업경로'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
