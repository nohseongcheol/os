#!/usr/bin/env python3
"""기존 pfad 호환 eintragPunkt. tatsächlichDaten umsetzung: ../Werkzeuge/fTPPrüfung.py"""
import importlib as entnehmenWert
import sys as betriebSystemWert
from pathlib import Path as pfad
betriebSystemWert.path.insert(0, str(pfad(__file__).resolve().parents[1] / 'Werkzeuge'))
if __name__ == '__main__':
    import runpy as ProgrammStarter
    ProgrammStarter.run_module('fTPPrüfung', run_name='__main__', alter_sys=True)
else:
    umsetzung = entnehmenWert.import_module('fTPPrüfung')
    zuordnungWert = {'timeout': 'ausführungZeitüberschreitung', 'payload': 'nutzdatenDaten', 'broken': 'beschädigt', 'linux_example': 'linuxBeispiel', 'chunk': 'fragmentWert', 'data': 'Daten', 'proc': 'prozess', 'code': 'befehlswortFolge', 'linux': 'linuxDatei', 'archive': 'archiv', 'main': 'ausführenVorgang', 'net_source': 'netzQuelltext', 'temporary': 'vorläufig', 'static_source': 'statischQuelltext', 'java_source': 'javaQuelltext', 'echo': 'wiedergebenDienstanbieterEintrag', 'ROOT': 'projektWurzel', 'text': 'Text', 'marker': 'markierung', 'EchoFixture': 'WiedergebenPrüfaufbau', 'command': 'befehl', 'out': 'ergebnisDaten', 'expected': 'erwartet', 'server_source': 'dienstanbieterQuelltext', 'shell': 'befehlshülle', 'upload': 'hochladenDateien', 'transcript': 'ablaufprotokoll', 'port': 'portNummer', 'native': 'systemnah', 'elf': 'ausführdateiDatei', 'server_udp_port': 'dienstanbieterDatagrammPort', 'packed': 'gepackt', 'bridge': 'brücke', 'selector': 'auswähler', 'end': 'endeVersatzwert', 'e': 'hilfsEintrag', 'ftp': 'dateiÜbertragungVerbindung', 'key': 'gedrücktWert', 'bytecode': 'bytecode', 'peer': 'gegenstelleWert', 'result': 'ergebnis', 'unchanged': 'bewahrtDaten', 'line': 'zeile', 'server_tcp_port': 'dienstanbieterDatenstromPort', 'source': 'ursprünglichDaten', 'NetworkBridge': 'netzwerkBrücke', 'jar': 'javaBündel', 'receive': 'nachrichtEmpfangen', 'report': 'validierungBericht'}
    for vorherigElementeintrag, aktuellElementeintrag in zuordnungWert.items():
        if hasattr(umsetzung, aktuellElementeintrag): globals()[vorherigElementeintrag] = getattr(umsetzung, aktuellElementeintrag)
