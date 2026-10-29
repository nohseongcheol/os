#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/terminalSchriftartErzeugenAbbild.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('terminalSchriftartErzeugenAbbild', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('terminalSchriftartErzeugenAbbild')
    zuordnungWert = {'data': 'Daten', 'img': 'Zeichnung', 'bits': 'bitlisteListe', 'x': 'waagerechteKoordinateKoordinate', 'draw': 'bildschirmZeichnen', 'licences': 'lizenzen', 'paths': 'pfadListe', 'y': 'senkrechteKoordinateKoordinate', 'main': 'ausführenVorgang', 'src': 'ursprünglichAdresse', 'fonts': 'schriftartListe', 'ROOT': 'projektWurzel', 'p': 'datenPosition', 'cp': 'zeichenKodierung', 'target': 'zielobjektWert'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
