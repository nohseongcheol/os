#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/arbeitsflächePrüfung.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('arbeitsflächePrüfung', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('arbeitsflächePrüfung')
    zuordnungWert = {'x': 'waagerechteKoordinateKoordinate', 'typing': 'eingegebenZeichen', 'message': 'mitteilungText', 'start': 'ausführenVorgang', 'down': 'istDrückend', 'exact': 'exaktWert', 'i': 'ordnungszahlIndex', 'press': 'drückenTaste', 'rectangles': 'rechtecklisteListe', 'sym': 'symbol', 'j': 'innerlichOrdnungszahl', 'deadline': 'fristZeit', 'proc': 'prozess', 'data': 'Daten', 'main': 'ausführenVorgang', 'w': 'angefordertBreiteWert', 'init': 'anfänglichWert', 'block': 'datenBlock', 'ROOT': 'projektWurzel', 'text': 'Text', 'marker': 'markierung', 'report': 'validierungBericht', 'until': 'bis', 'clipboard': 'zwischenablageWert', 'dst': 'zielAdresse', 'seen': 'gesehenEinträge', 'poll': 'bereitschaftÜberwacher', 'transcript': 'ablaufprotokoll', 'port': 'portNummer', 'offset': 'versatzwertWert', 'h': 'angefordertHöheWert', 'src': 'ursprünglichAdresse', 'event': 'ereignis', 'encoding': 'Zeichensatz', 'size': 'größe', 'key': 'gedrücktWert', 'pixels': 'bildpunkteListe', 'y': 'senkrechteKoordinateKoordinate', 'output': 'ausgabe', 'symbol': 'symbolWert', 'client': 'anfragestelle', 'char': 'zeichenDaten', 'rgb': 'rGBFarbe'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
