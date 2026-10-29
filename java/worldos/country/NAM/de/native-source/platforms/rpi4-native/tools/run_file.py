#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/dateiAusführen.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('dateiAusführen', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('dateiAusführen')
    zuordnungWert = {'timeout': 'ausführungZeitüberschreitung', 's': 'zeichenketteDaten', 'i': 'ordnungszahlIndex', 'match': 'istGleich', 'files': 'dateiListe', 'program': 'programm', 'executable': 'ausführdateiAbbild', 'args': 'argumentDatenfeld', 'chunk': 'fragmentWert', 'data': 'Daten', 'proc': 'prozess', 'send': 'senden', 'main': 'ausführenVorgang', 'marker': 'markierung', 'command': 'befehl', 'include': 'einbinden', 'dumped': 'ausgelesen', 'run': 'befehlAusführen', 'p': 'datenPosition', 'parser': 'strukturanalysierer', 'options': 'wahlmöglichkeiten', 'kind': 'kategorieWert', 'selector': 'auswähler', 'upload_data': 'hochladenDaten', 'end': 'endeVersatzwert', 'n': 'elementeintragAnzahl', 'd': 'zielDaten', 'key': 'gedrücktWert', 'output': 'ausgabe', 'line': 'zeile', 'name': 'Name', 'upload_name': 'hochladenName', 'receive': 'nachrichtEmpfangen'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
