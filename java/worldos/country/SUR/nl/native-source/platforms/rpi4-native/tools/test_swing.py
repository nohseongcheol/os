#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/test_Swing.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('test_Swing', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('test_Swing')
    toewijzing_WAARDE = {'wait': '기다리기', 'x': 'x_coördinaat', 's': 'tekenreeks_gegevens', 'i': '순번', 'sel': 'selector_a916db4e', 'seconds': '초단위', 'log': 'LOG_RECORD', 'data': 'gegevens', 'at': 'actueel_functie', 'send': 'e_mailen', 'main': 'starten', 'req': 'aanvraag_WAARDE', 'hot': 'alias_WAARDE', 'pump': 'greep_gebeurtenis', 'ROOT': 'Taken_wortel', 'marker': 'markering', 'b': 'SECONDE_WAARDE', 'command': 'opdracht', 'shell': 'Shell', 'f': 'Bestand_invoer', 'click': 'click_knop', 'k': '셋째순번', 'c': 'codepoint', 'r': '반환값', 'p': 'gegevens_functie', 'command_mode': 'opdracht_MODUS', 'end': 'beëindigen_VERSCHUIVING', 'classes': 'les_pad', 'key': '누름값', 'y': 'Y_coördinaat', 'result': 'resultaat', 'report': 'validatie_Rapport', 'dest': 'doel_WAARDE_functie', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
