#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/netzwerkBrücke.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('netzwerkBrücke', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('netzwerkBrücke')
    zuordnungWert = {'response': 'rückmeldung', 'parts': 'pfadBaustein', 's': 'zeichenketteDaten', 'i': 'ordnungszahlIndex', 'close': 'schließen', 'forward': 'weiterleitendRegel', 'slip_input': 'sLIPEingabe', 'self': 'selbstWert', 'item': 'eintragWert', 'flags': 'konfigurationBitliste', 'ftp_port': 'dateiÜbertragungPortNummer', 'args': 'argumentDatenfeld', 'server': 'dienstanbieterWert', 'data': 'Daten', 'ethernet_input': 'ethernetEingabe', 'trace_packet': 'spurPaket', 'GATEWAY': 'netzübergangHardwareAdresse', 'rule': 'regelWert', 'protocol': 'NetzwerkABI', 'forwards': 'weiterleitendRegeln', 'occupied': 'belegt', 'host': 'Wirtssystem', 'ack': 'bestätigungNummer', 'serial_port': 'seriellPortNummer', 'readers': 'leserListe', 'guest': 'gast', 'destination': 'zielDatenAdresse', 'ethernet_port': 'ethernetPort', 'b': 'zweiterWert', 'MAC': 'maschineAdresse', 'arp': 'adresseAuflösungPaket', 'writable': 'beschreibbar', 'direction': 'richtung', 'seq': 'reihenfolgeNummer', 'frame': 'ausführungRahmen', 'loop': 'zyklusWert', 'port': 'portNummer', 'offset': 'versatzwertWert', 'readable': 'kannLesen', 'c': 'zeichenKode', 'p': 'datenPosition', 'writers': 'schreiberListe', 'IP': 'internetAdresseWert', 'e': 'hilfsEintrag', 'n': 'elementeintragAnzahl', 'packet': 'paketDaten', 'arguments': 'weitergeleitetArgument', 'source': 'ursprünglichDaten', 'NetworkBridge': 'netzwerkBrücke', 'window': 'fenster', 'capture': 'erfassen'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
