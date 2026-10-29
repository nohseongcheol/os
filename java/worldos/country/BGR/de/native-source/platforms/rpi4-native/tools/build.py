#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/systemErzeugenAbbild.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('systemErzeugenAbbild', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('systemErzeugenAbbild')
    zuordnungWert = {'network': 'netzwerk', 'BUILD': 'pfadErzeugenAbbild', 'ar': 'archivWerkzeug', 'build_examples': 'beispielsammlungErstellen', 'posix': 'pOSIX', 'font_data': 'schriftartDaten', 'flags': 'konfigurationBitliste', 'a': 'ersterWert', 'cc': 'CÜbersetzer', 'args': 'argumentDatenfeld', 'source_flags': 'ursprünglichKonfiguration', 'ld': 'binderWerkzeug', 'method': 'methodeEintrag', 'main': 'ausführenVorgang', 'objcopy': 'objektDateiUmwandler', 'ROOT': 'projektWurzel', 'cxx': 'cppÜbersetzer', 'includes': 'einschlüsse', 'compiler': 'übersetzerWerkzeug', 'build_users': 'benutzerRaumErstellen', 'f': 'dateiEintrag', 'extra': 'zusätzlichGebiet', 'exports': 'exportierenTabelle', 'jobs': 'aufträgeErzeugenAbbild', 'run': 'befehlAusführen', 'path': 'pfad', 'REPO': 'ablageWurzel', 'tool': 'Werkzeuge', 'classes': 'klassePfad', 'output': 'ausgabe', 'samples': 'beispielEinträge', 'symbol': 'symbolWert', 'source': 'ursprünglichDaten', 'name': 'Name', 'build_network': 'netzwerkErstellen', 'font_info': 'schriftartInformation', 'manifest': 'bündelInhaltsverzeichnis', 'work': 'arbeitendPfad'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
