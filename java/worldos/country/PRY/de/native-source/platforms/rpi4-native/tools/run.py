#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/befehlAusführen.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('befehlAusführen', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('befehlAusführen')
    zuordnungWert = {'supported': 'unterstütztMerkmale', 'parser': 'strukturanalysierer', 'qemu': 'AttrappeMaschine', 'run_desktop': 'arbeitsflächeAusführenVorgang', 'main': 'ausführenVorgang', 'host': 'Wirtssystem', 'status': 'statuswertWert', 'NetworkBridge': 'netzwerkBrücke', 'ROOT': 'projektWurzel', 'bridge': 'brücke', 'loader': 'lader', 'base': 'hintergrundWert', 'options': 'wahlmöglichkeiten', 'binary': 'binär', 'args': 'argumentDatenfeld', 'command': 'befehl'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
