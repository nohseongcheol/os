#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/javaBibliothekErzeugenAbbild.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('javaBibliothekErzeugenAbbild', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('javaBibliothekErzeugenAbbild')
    zuordnungWert = {'header': 'kopfbereichWert', 'sources': 'Quelltextliste', 'i': 'ordnungszahlIndex', 'info': 'systemInformation', 'payload': 'nutzdatenDaten', 'src': 'ursprünglichAdresse', 'run': 'befehlAusführen', 'build_java_library': 'javaBibliothekErstellen', 'relative': 'relativPfad', 'classes': 'klassePfad', 'dist': 'verteilungPfad', 'archive': 'archiv', 'output': 'ausgabe', 'root': 'wurzelAdresse', 'name': 'Name', 'jar': 'javaBündel', 'b': 'zweiterWert', 'entries': 'einträgeListe'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
