#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/jVMPrüfung.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('jVMPrüfung', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('jVMPrüfung')
    zuordnungWert = {'message': 'mitteilungText', 's': 'zeichenketteDaten', 'actual': 'tatsächlichErgebnis', 'match': 'istGleich', 'payload': 'nutzdatenDaten', 'cases': 'fallPrüfung', 'fixture': 'datenPrüfung', 'main': 'ausführenVorgang', 'ROOT': 'projektWurzel', 'text': 'Text', 'valid': 'gültig', 'includes': 'einschlüsse', 'include': 'einbinden', 'expected': 'erwartet', 'sources': 'Quelltextliste', 'tmp': 'vorläufigPfad', 'done': 'abgeschlossenGesamtmenge', 'classes': 'klassePfad', 'output': 'ausgabe', 'result': 'ergebnis', 'cmd': 'befehlArgumente', 'name': 'Name', 'jar': 'javaBündel', 'report': 'validierungBericht', 'tests': 'listePrüfung'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
