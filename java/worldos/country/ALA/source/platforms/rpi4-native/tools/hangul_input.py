#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/한글입력.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('한글입력')
    mappning_värde = {'old': 'Föregående_objekt', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'Nyckel_Layout', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': 'incheckning_komposition', 'feed': 'feed_Nyckel', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'skicka', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Historik', 'pair': '한쌍', 'char': 'teckendata', 'VOWEL': '가운뎃소리목록', 'right': 'HÖGER', 'value': 'värde', 'text': 'text'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
