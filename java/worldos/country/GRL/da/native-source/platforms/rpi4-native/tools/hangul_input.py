#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/한글입력.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('한글입력')
    tilknytning_VÆRDI = {'old': 'Forrige_vare', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'tast_Layout', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': 'udføre_komposition', 'feed': 'feed_tast', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'maile', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Historik', 'pair': '한쌍', 'char': 'tegndata', 'VOWEL': '가운뎃소리목록', 'right': 'HØJRE', 'value': 'VÆRDI', 'text': 'Tekst'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
