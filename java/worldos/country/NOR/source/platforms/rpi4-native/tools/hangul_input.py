#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/한글입력.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('한글입력')
    tildeling_VERDI = {'old': 'Forrige_vare', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'tast_Oppsett', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': '조합확정', 'feed': 'feed_tast', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'sende', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Logg', 'pair': '한쌍', 'char': 'tegndata', 'VOWEL': '가운뎃소리목록', 'right': 'HØYRE', 'value': 'VERDI', 'text': 'Tekst'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
