#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/arbeitsflächeAnsicht.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('arbeitsflächeAnsicht', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('arbeitsflächeAnsicht')
    zuordnungWert = {'count': 'eintragAnzahl', 'special': 'besondersTaste', 'error': 'fehler', 'exact': 'exaktWert', 'network': 'netzwerk', 'closed': 'istGeschlossen', 'length': 'Länge', 'opened': 'geöffnet', 'ftp_port': 'dateiÜbertragungPortNummer', 'server': 'dienstanbieterWert', 'resources': 'betriebsmittel', 'data': 'Daten', 'shift': 'verschiebenTaste', 'send': 'senden', 'run_desktop': 'arbeitsflächeAusführenVorgang', 'protocol': 'NetzwerkABI', 'forwards': 'weiterleitendRegeln', 'host': 'Wirtssystem', 'text': 'Text', 'korean': 'koreanisch', 'port': 'portNummer', 'signum': 'signalNummer', 'version': 'versionNummer', 'parser': 'strukturanalysierer', 'bridge': 'brücke', 'kind': 'kategorieWert', 'tail': 'endungTeil', 'size': 'größe', 'previous_buttons': 'vorherigSchaltflächen', 'key': 'gedrücktWert', 'y': 'senkrechteKoordinateKoordinate', 'prefix': 'voranstehendTeil', 'client': 'anfragestelle', 'char': 'zeichenDaten', 'work': 'arbeitendPfad', 'Keyboard': 'Tastatur', 'x': 'waagerechteKoordinateKoordinate', 'down': 'istDrückend', 'net': 'netzwerkBrückeEintrag', 'self': 'selbstWert', 'mode_changed': 'betriebsartGeändert', 'serial': 'seriellEinAusgabe', 'args': 'argumentDatenfeld', 'Hangul': 'hangulZusammensetzen', 'chunk': 'fragmentWert', 'proc': 'prozess', 'Desktop': 'arbeitsflächeVerbinden', 'buttons': 'schaltflächen', 'thread': 'hintergrundarbeiter', 'pressed': 'istGedrückt', 'previous': 'vorherig', 'toggle': 'umschaltenBetriebsart', 'command': 'befehl', 'sock': 'netzbuchseWert', 'frame': 'ausführungRahmen', 'ctrl': 'steuerungTaste', 'path': 'pfad', 'cp': 'zeichenKodierung', 'terminate': 'beendenProzess', 'security': 'sicherheit', 'vnc_port': 'vNCPort', 'body': 'rumpfText', 'index': 'nachschlagenIndex', 'exited': 'hatVerlassen', 'keysym': 'tasteSymbol', 'output': 'ausgabe', 'keyboard': 'tastaturEintrag', 'interrupted': 'unterbrochen', 'listener': 'portEmpfangen', 'reader': 'leser', 'NetworkBridge': 'netzwerkBrücke', 'gui': 'zeichnungBildschirm', 'worker': 'verarbeitungAufgabe'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
