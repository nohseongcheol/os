#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/abbildErstellen.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('abbildErstellen', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('abbildErstellen')
    zuordnungWert = {'total': 'gesamtwertKapazität', 'start': 'ausführenVorgang', 'firmware': 'geräteprogrammWert', 'files': 'dateiListe', 'archive_base': 'archivBasis', 'partition': 'partitionDatei', 'archive': 'archiv', 'main': 'ausführenVorgang', 'block': 'datenBlock', 'ROOT': 'projektWurzel', 'boot': 'startvorgangPfad', 'stage': 'stufeWert', 'out': 'ergebnisDaten', 'expected': 'erwartet', 'f': 'dateiEintrag', 'src': 'ursprünglichAdresse', 'path': 'pfad', 'p': 'datenPosition', 'extracted': 'extrahiert', 'member': 'mitglied', 'mbr': 'LeitstelleStartvorgangAufzeichnung', 'image': 'abbild', 'sector_count': 'sektorAnzahl', 'dist': 'verteilungPfad', 'sha': 'prüfsummeBerechnen', 'license_': 'lizenz', 'source': 'ursprünglichDaten', 'name': 'Name', 'value': 'Wert', 'manifest': 'bündelInhaltsverzeichnis', 'dest': 'zielWertPosition', 'work': 'arbeitendPfad'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
