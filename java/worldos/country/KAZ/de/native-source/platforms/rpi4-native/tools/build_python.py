#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/pythonErzeugenAbbild.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('pythonErzeugenAbbild', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('pythonErzeugenAbbild')
    zuordnungWert = {'ld': 'binderWerkzeug', 'archive': 'archiv', 'SHA256': 'validierungPrüfsumme', 'build_python': 'pythonErstellen', 'root': 'wurzelAdresse', 'source': 'ursprünglichDaten', 'name': 'Name', 'path': 'pfad', 'VERSION': 'ausgabeversionWert', 'cc': 'CÜbersetzer', 'tar': 'tARBündel', 'newlib': 'newlib', 'member': 'mitglied'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
