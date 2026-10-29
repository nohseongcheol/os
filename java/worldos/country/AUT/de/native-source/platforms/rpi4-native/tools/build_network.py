#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/netzwerkErzeugenAbbild.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('netzwerkErzeugenAbbild', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('netzwerkErzeugenAbbild')
    zuordnungWert = {'obj': 'zielDatei', 'objects': 'zielDateien', 'library': 'bibliothek', 'output': 'ausgabe', 'port': 'portNummer', 'root': 'wurzelAdresse', 'files': 'dateiListe', 'source': 'ursprünglichDaten', 'run': 'befehlAusführen', 'flags': 'konfigurationBitliste', 'path': 'pfad', 'build_network': 'netzwerkErstellen', 'cc': 'CÜbersetzer', 'ar': 'archivWerkzeug'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
