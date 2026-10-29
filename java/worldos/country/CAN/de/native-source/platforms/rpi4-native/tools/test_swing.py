#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/swingPrüfung.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('swingPrüfung', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('swingPrüfung')
    zuordnungWert = {'wait': 'abwarten', 'x': 'waagerechteKoordinateKoordinate', 's': 'zeichenketteDaten', 'i': 'ordnungszahlIndex', 'sel': 'Auswähler', 'seconds': 'sekundenEinheit', 'log': 'protokolldateiAufzeichnung', 'data': 'Daten', 'at': 'aktuellPosition', 'send': 'senden', 'main': 'ausführenVorgang', 'req': 'anfrageWert', 'hot': 'kurzwegWert', 'pump': 'kennwertEreignis', 'ROOT': 'projektWurzel', 'marker': 'markierung', 'b': 'zweiterWert', 'command': 'befehl', 'shell': 'befehlshülle', 'f': 'dateiEintrag', 'click': 'klickenSchaltfläche', 'k': 'dritterIndex', 'c': 'zeichenKode', 'r': 'zurückgegebenWert', 'p': 'datenPosition', 'command_mode': 'befehlBetriebsart', 'end': 'endeVersatzwert', 'classes': 'klassePfad', 'key': 'gedrücktWert', 'y': 'senkrechteKoordinateKoordinate', 'result': 'ergebnis', 'report': 'validierungBericht', 'dest': 'zielWertPosition', 'work': 'arbeitendPfad', 'qmp': 'attrappeSteuerungVerbindung'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
