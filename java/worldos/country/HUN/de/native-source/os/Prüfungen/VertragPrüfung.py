#!/usr/bin/env python3
"""Wirtssystem libc 없이 연결한 Deutsch C 프로그램을 tatsächlichDaten ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from benutzerNetzwerkPrüfung import VirtuelleMaschine

position = Path(__file__).resolve().parents[1]

def befehlAusführen():
    ergebnis = {}
    dienstanbieterWert = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dienstanbieterWert.bind(('127.0.0.1', 0))
    dienstanbieterWert.settimeout(0.1)
    portNummer = dienstanbieterWert.getsockname()[1]
    empfangenWertDaten = []
    beendigungStatuswert = threading.Event()
    def wiedergebenAntwort():
        while not beendigungStatuswert.is_set():
            try:
                Daten, adresse = dienstanbieterWert.recvfrom(4096)
            except socket.timeout:
                continue
            empfangenWertDaten.append(Daten)
            dienstanbieterWert.sendto(Daten, adresse)
    hintergrundarbeiterWert = threading.Thread(target=wiedergebenAntwort, daemon=True)
    hintergrundarbeiterWert.start()
    try:
        for artWert in ('elf', 'iso'):
            maschine = VirtuelleMaschine(position / ('build/kernel.' + artWert), artWert)
            try:
                for wiederholungsschrittWert in range(2):
                    maschine.befehl('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    maschine.befehl('run posixudp ' + str(portNummer), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ausführenVorgang = len(maschine.protokolldateiAufzeichnung)
                maschine.seriellWert.sendall(b'run posixinput\n')
                maschine.statuswertWarten('POSIX INPUT READY', ausführenVorgang)
                maschine.seriellWert.sendall(b'abcdef')
                Ausgabe = maschine.statuswertWarten('jkoros> ', ausführenVorgang)
                assert 'POSIX INPUT PASS' in Ausgabe and 'Exit: 0' in Ausgabe, Ausgabe
                maschine.befehl('javac Hello.java', ['Exit: 0'])
                maschine.befehl('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                maschine.befehl('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ergebnis[artWert] = maschine.protokolldateiAufzeichnung.decode('utf-8', 'replace')
                print('PASS:', artWert, 'POSIX Datei/공유 position/삭제 수명/adresse wertSchützen/UDP/표준 Eingabewert/기존 Java', flush=True)
            finally:
                maschine.schließen()
        assert b'posix-udp' in empfangenWertDaten and b'truncate' in empfangenWertDaten and b'' in empfangenWertDaten
    finally:
        beendigungStatuswert.set(); hintergrundarbeiterWert.join(timeout=2); dienstanbieterWert.close()
    ergebnis['host_datagrams'] = [Daten.decode() for Daten in empfangenWertDaten]
    (position / 'build/VertragPrüfung.json').write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    befehlAusführen()
