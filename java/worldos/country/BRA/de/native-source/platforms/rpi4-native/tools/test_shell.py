#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/befehlshüllePrüfung.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('befehlshüllePrüfung', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('befehlshüllePrüfung')
    zuordnungWert = {'timeout': 'ausführungZeitüberschreitung', 'x': 'waagerechteKoordinateKoordinate', 'msg': 'netzwerkNachricht', 'i': 'ordnungszahlIndex', 'reply': 'antwort', 'call': 'aufrufen', 'args': 'argumentDatenfeld', 'chunk': 'fragmentWert', 'data': 'Daten', 'proc': 'prozess', 'long_text': 'langText', 'restored': 'wiederhergestelltDaten', 'send': 'senden', 'file': 'Datei', 'main': 'ausführenVorgang', 'found': 'ergebnisSuchen', 'ROOT': 'projektWurzel', 'text': 'Text', 'marker': 'markierung', 'command': 'befehl', 'expected': 'erwartet', 'pixel': 'bildpunkt', 'shell': 'befehlshülle', 'poll': 'bereitschaftÜberwacher', 'transcript': 'ablaufprotokoll', 'end': 'endeVersatzwert', 'image': 'abbild', 'key': 'gedrücktWert', 'y': 'senkrechteKoordinateKoordinate', 'output': 'ausgabe', 'result': 'ergebnis', 'client': 'anfragestelle', 'line': 'zeile', 'stream': 'datenstromWert', 'name': 'Name', 'value': 'Wert', 'receive': 'nachrichtEmpfangen', 'report': 'validierungBericht', 'work': 'arbeitendPfad', 'qmp': 'attrappeSteuerungVerbindung'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
