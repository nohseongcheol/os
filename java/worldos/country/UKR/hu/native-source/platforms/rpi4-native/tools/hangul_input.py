#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/한글입력.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('한글입력')
    leképezés_ÉRTÉK = {'old': 'Előző_cikk', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'Kulcs_Navigáció', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': 'véglegesít_rész_egész', 'feed': 'csatorna_Kulcs', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'küld', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Előzmények', 'pair': '한쌍', 'char': 'karakteres_adat', 'VOWEL': '가운뎃소리목록', 'right': 'jog', 'value': 'ÉRTÉK', 'text': 'Szöveg'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
