#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/한글입력.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('한글입력')
    toewijzing_WAARDE = {'old': 'Vorige_item', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'toets_Indeling', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': 'doorvoeren_samenstelling', 'feed': 'feed_toets', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'e_mailen', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Geschiedenis', 'pair': '한쌍', 'char': 'tekengegevens', 'VOWEL': '가운뎃소리목록', 'right': 'recht', 'value': 'WAARDE', 'text': 'tekst'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
