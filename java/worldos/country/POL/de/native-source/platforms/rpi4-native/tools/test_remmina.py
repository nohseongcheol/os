#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/remminaPrüfung.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('remminaPrüfung', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('remminaPrüfung')
    zuordnungWert = {'wait': 'abwarten', 'typing': 'eingegebenZeichen', 'start': 'ausführenVorgang', 'profile': 'profil', 'focused': 'fokussiert', 'serial': 'seriellEinAusgabe', 'keys': 'gedrücktTasten', 'server': 'dienstanbieterWert', 'log': 'protokolldateiAufzeichnung', 'args': 'argumentDatenfeld', 'deadline': 'fristZeit', 'data': 'Daten', 'candidate': 'kandidat', 'logs': 'protokolldateiAufzeichnungen', 'kw': 'benanntArgument', 'number': 'numerischWert', 'main': 'ausführenVorgang', 'ready': 'vorbereitungFertig', 'found': 'ergebnisSuchen', 'guest': 'gast', 'ROOT': 'projektWurzel', 'marker': 'markierung', 'text': 'Text', 'out': 'ergebnisDaten', 'env': 'umgebung', 'f': 'dateiEintrag', 'port': 'portNummer', 'offset': 'versatzwertWert', 'version': 'versionNummer', 'p': 'datenPosition', 'selector': 'auswähler', 'xvfb': 'virtuellDarstellen', 'display': 'darstellenGerät', 'n': 'elementeintragAnzahl', 'key': 'gedrücktWert', 'processes': 'laufendProzesse', 'rootfs': 'wurzeldateisystem', 'xdo': 'virtuellEingabeWerkzeug', 'name': 'Name', 'window': 'fenster', 'report': 'validierungBericht', 'work': 'arbeitendPfad'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
