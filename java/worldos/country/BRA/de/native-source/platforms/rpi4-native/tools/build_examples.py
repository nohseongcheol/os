#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/beispielsammlungErzeugenAbbild.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('beispielsammlungErzeugenAbbild', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('beispielsammlungErzeugenAbbild')
    zuordnungWert = {'out': 'ergebnisDaten', 'build_examples': 'beispielsammlungErstellen', 'files': 'dateiListe', 'java': 'javaAusführen', 'run': 'befehlAusführen', 'path': 'pfad', 'p': 'datenPosition', 'readme': 'liesmich', 'build_java_library': 'javaBibliothekErstellen', 'code': 'befehlswortFolge', 'index': 'nachschlagenIndex', 'classes': 'klassePfad', 'repo': 'ablagePfad', 'root': 'wurzelAdresse', 'content': 'inhaltswertWert', 'source': 'ursprünglichDaten', 'name': 'Name', 'target': 'zielobjektWert', 'manifest': 'bündelInhaltsverzeichnis', 'language': 'Sprache'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
