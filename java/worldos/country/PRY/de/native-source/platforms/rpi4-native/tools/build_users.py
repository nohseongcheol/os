#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/benutzerRaumErzeugenAbbild.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('benutzerRaumErzeugenAbbild', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('benutzerRaumErzeugenAbbild')
    zuordnungWert = {'mode': 'methodeBetriebsart', 'header': 'kopfbereichWert', 'i': 'ordnungszahlIndex', 'build_ccompiler': 'cÜbersetzerErstellen', 'ar': 'archivWerkzeug', 'posix': 'pOSIX', 'payload': 'nutzdatenDaten', 'flags': 'konfigurationBitliste', 'cases': 'fallPrüfung', 'cc': 'CÜbersetzer', 'data': 'Daten', 'build_java_library': 'javaBibliothekErstellen', 'ld': 'binderWerkzeug', 'repo': 'ablagePfad', 'build_python': 'pythonErstellen', 'inc': 'einbindenPfad', 'argument': 'weitergeleitetWert', 'text': 'Text', 'headers': 'kopfListe', 'cxx': 'cppÜbersetzer', 'valid': 'gültig', 'build': 'erzeugenAbbild', 'build_users': 'benutzerRaumErstellen', 'compiler': 'übersetzerWerkzeug', 'uzlib': 'entpackbibliothek', 'extra': 'zusätzlichGebiet', 'phoff': 'programmKopfVersatzwert', 'offset': 'versatzwertWert', 'text_address': 'befehlAdresse', 'abi': 'AufrufVorgangABI', 'assembly': 'assemblersprache', 'run': 'befehlAusführen', 'path': 'pfad', 'p': 'datenPosition', 'changed': 'geändert', 'n': 'elementeintragAnzahl', 'flag': 'einstellungenWert', 'index': 'nachschlagenIndex', 'classes': 'klassePfad', 'output': 'ausgabe', 'loads': 'ladeeinträge', 'data_address': 'datenAdresse', 'symbol': 'symbolWert', 'root': 'wurzelAdresse', 'patches': 'änderungen', 'source': 'ursprünglichDaten', 'sizes': 'größen', 'blobs': 'binärblöcke', 'name': 'Name', 'value': 'Wert', 'fmt': 'datenFormat', 'work': 'arbeitendPfad'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
