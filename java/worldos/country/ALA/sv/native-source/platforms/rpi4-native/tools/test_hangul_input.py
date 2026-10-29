#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/한글입력시험.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('한글입력시험', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('한글입력시험')
    mappning_värde = {'expected': '예상결과', 'Keyboard': 'tangentbord', 'press': 'tryck_Nyckel', 'self': '자신', 'test_modes_repeat_and_commit': 'test_전환반복확정', 'keys': '누름열', 'test_paste_and_unicode': 'test_klistra_in_AND_UNICODE', 'data': 'data', 'key': '누름값', 'send': 'skicka', 'test_words': 'test_낱말', 'InputTests': '한글입력시험', 'test_backspace': 'test_앞글자지우기', 'symbol': 'symbol_värde', 'char': 'teckendata', 'type': 'Typ_område'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
