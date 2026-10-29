#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/cÜbersetzerErzeugenAbbild.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('cÜbersetzerErzeugenAbbild', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('cÜbersetzerErzeugenAbbild')
    zuordnungWert = {'out': 'ergebnisDaten', 'builtins': 'einbauten', 'header': 'kopfbereichWert', 'sdk': 'entwicklungWerkzeugsatz', 'build_ccompiler': 'cÜbersetzerErstellen', 'i': 'ordnungszahlIndex', 'elf': 'ausführdateiDatei', 'run': 'befehlAusführen', 'flags': 'konfigurationBitliste', 'path': 'pfad', 'p': 'datenPosition', 'cc': 'CÜbersetzer', 'obj': 'zielDatei', 'flag': 'einstellungenWert', 'ld': 'binderWerkzeug', 'objects': 'zielDateien', 'repo': 'ablagePfad', 'v': 'vorläufigDaten', 'upstream': 'vorgelagert', 'root': 'wurzelAdresse', 'assets': 'bestandteile', 'source': 'ursprünglichDaten', 'name': 'Name', 'includes': 'einschlüsse'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
