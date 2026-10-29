#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/eLFPrüfung.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('eLFPrüfung', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('eLFPrüfung')
    zuordnungWert = {'out': 'ergebnisDaten', 'expected': 'erwartet', 'phoff': 'programmKopfVersatzwert', 'offset': 'versatzwertWert', 'invalid': 'ungültigDaten', 'path': 'pfad', 'executable': 'ausführdateiAbbild', 'rejected': 'zurückweisungErgebnis', 'linux_example': 'linuxBeispiel', 'original': 'ursprünglich', 'result': 'ergebnis', 'format_': 'formatFestlegen', 'main': 'ausführenVorgang', 'content': 'inhaltswertWert', 'source': 'ursprünglichDaten', 'name': 'Name', 'reference': 'vergleichGrundlinie', 'ROOT': 'projektWurzel', 'value': 'Wert', 'report': 'validierungBericht'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
