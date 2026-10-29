#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/test_Swing.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('test_Swing', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('test_Swing')
    mappning_värde = {'wait': '기다리기', 'x': 'x_koordinat', 's': 'sträng_data', 'i': '순번', 'sel': 'väljare_a916db4e', 'seconds': '초단위', 'log': 'LOG_POST', 'data': 'data', 'at': 'aktuellt_placera', 'send': 'skicka', 'main': 'Kör', 'req': 'begäran_värde', 'hot': 'alias_värde', 'pump': 'handtag_händelse', 'ROOT': 'åtgärd_rot', 'marker': 'markör_8b722c5f', 'b': 'SEKUND_värde', 'command': 'kommando', 'shell': 'Shell', 'f': 'fil_post', 'click': 'klick_knapp', 'k': '셋째순번', 'c': 'kodpunkt', 'r': '반환값', 'p': 'data_placera', 'command_mode': 'kommando_läge', 'end': 'avsluta_FÖRSKJUTNING', 'classes': 'Kurs_väg', 'key': '누름값', 'y': 'Y_koordinat', 'result': 'RESULTAT', 'report': 'validering_Rapport', 'dest': 'mål_värde_placera', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
