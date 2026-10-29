#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/exportierenSDK.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('exportierenSDK', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('exportierenSDK')
    zuordnungWert = {'out': 'ergebnisDaten', 'obj': 'zielDatei', 'relative': 'relativPfad', 'compiler_archive': 'übersetzerArchiv', 'sdk': 'entwicklungWerkzeugsatz', 'dist': 'verteilungPfad', 'archive': 'archiv', 'main': 'ausführenVorgang', 'posix': 'pOSIX', 'files': 'dateiListe', 'source': 'ursprünglichDaten', 'name': 'Name', 'target': 'zielobjektWert', 'ROOT': 'projektWurzel', 'destination': 'zielDatenAdresse', 'manifest': 'bündelInhaltsverzeichnis', 'work': 'arbeitendPfad'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
