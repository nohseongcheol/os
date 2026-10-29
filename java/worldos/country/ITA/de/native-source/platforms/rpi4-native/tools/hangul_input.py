#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/hangulEingabe.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('hangulEingabe', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('hangulEingabe')
    zuordnungWert = {'old': 'vorherigElementeintrag', 'backspace': 'rückschritt', 'committed': 'bestätigt', 'KEYS': 'tasteAnordnung', 'self': 'selbstWert', 'FINALS': 'zusammengesetztesWortAbschließendHangulBuchstabe', 'VOWELS': 'zusammengesetztesWortMittellautHangulBuchstabe', 'INITIAL': 'anfänglichHangulBuchstabeTabelle', 'initial': 'anfänglichHangulBuchstabe', 'commit': 'bestätigenZusammensetzung', 'feed': 'zuführenTaste', 'vowel': 'mittellautHangulBuchstabe', 'Hangul': 'hangulZusammensetzen', 'SPLIT': 'abschließendHangulBuchstabeAufteilen', 'final': 'abschließendHangulBuchstabe', 'key': 'gedrücktWert', 'send': 'senden', 'left': 'linksSeiteRand', 'FINAL': 'abschließendHangulBuchstabeTabelle', 'history': 'verlauf', 'pair': 'einsPaar', 'char': 'zeichenDaten', 'VOWEL': 'mittellautHangulBuchstabeTabelle', 'right': 'rechts', 'value': 'Wert', 'text': 'Text'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
