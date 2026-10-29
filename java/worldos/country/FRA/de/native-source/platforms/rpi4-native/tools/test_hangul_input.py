#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/hangulEingabePrüfung.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('hangulEingabePrüfung', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('hangulEingabePrüfung')
    zuordnungWert = {'expected': 'erwartet', 'Keyboard': 'Tastatur', 'press': 'drückenTaste', 'self': 'selbstWert', 'test_modes_repeat_and_commit': 'betriebsartenWiederholenUndBestätigenPrüfung', 'keys': 'gedrücktTasten', 'test_paste_and_unicode': 'einsetzenUndUnicodePrüfung', 'data': 'Daten', 'key': 'gedrücktWert', 'send': 'senden', 'test_words': 'wörterPrüfung', 'InputTests': 'hangulEingabePrüfung', 'test_backspace': 'rückschrittPrüfung', 'symbol': 'symbolWert', 'char': 'zeichenDaten', 'type': 'typKategorie'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
