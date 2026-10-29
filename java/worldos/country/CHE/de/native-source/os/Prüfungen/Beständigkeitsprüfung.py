#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 bewahrtKopieren 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from benutzerNetzwerkPrüfung import VirtuelleMaschine

position = Path(__file__).resolve().parents[1]
vorgabe = importlib.util.spec_from_file_location('medienWerkzeug', position / 'Werkzeuge/SpeichermediumErstellen.py')
medienWerkzeug = importlib.util.module_from_spec(vorgabe)
vorgabe.loader.exec_module(medienWerkzeug)

def bearbeitenWert(maschine, inhaltswertWert):
    ausführenVorgang = len(maschine.protokolldateiAufzeichnung)
    maschine.seriellWert.sendall(('edit note.txt\n' + inhaltswertWert + '\n.save\n').encode())
    return maschine.statuswertWarten('jkoros> ', ausführenVorgang)

def befehlAusführen():
    ergebnis = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as vorläufigWert:
        medienWert = Path(vorläufigWert) / 'files.img'
        medienWerkzeug.eintragErstellen(medienWert)
        maschine = VirtuelleMaschine(position / 'build/kernel.elf', speichergerätMittelgroß=medienWert)
        try:
            maschine.befehl('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            bearbeitenWert(maschine, 'generation-one')
            maschine.befehl('sync', ['Sync: 0'])
            bearbeitenWert(maschine, 'generation-two')
            maschine.befehl('sync', ['Sync: 0'])
            bearbeitenWert(maschine, 'unsynced-three')
            ergebnis['save'] = maschine.protokolldateiAufzeichnung.decode('utf-8', 'replace')
        finally:
            maschine.schließen()
        maschine = VirtuelleMaschine(position / 'build/kernel.iso', 'iso', speichergerätMittelgroß=medienWert)
        try:
            Ausgabe = maschine.befehl('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Ausgabe
            maschine.befehl('cat stored.txt', ['saved-from-C'])
            ergebnis['restore'] = maschine.protokolldateiAufzeichnung.decode('utf-8', 'replace')
        finally:
            maschine.schließen()
        Daten = bytearray(medienWert.read_bytes())
        erzeugungsstufenListe = [struct.unpack_from('<I', Daten, (1 + Nummer * 259) * 512 + 4)[0] for Nummer in (0, 1)]
        neuesterWert = 0 if erzeugungsstufenListe[0] > erzeugungsstufenListe[1] else 1
        Daten[(1 + neuesterWert * 259 + 3) * 512] ^= 1
        medienWert.write_bytes(Daten)
        maschine = VirtuelleMaschine(position / 'build/kernel.elf', speichergerätMittelgroß=medienWert)
        try:
            maschine.befehl('cat note.txt', ['generation-one'])
            maschine.befehl('cat stored.txt', ['saved-from-C'])
            ergebnis['checksum_fallback'] = maschine.protokolldateiAufzeichnung.decode('utf-8', 'replace')
        finally:
            maschine.schließen()
        andererMedien = Path(vorläufigWert) / 'foreign.img'
        andererMedien.write_bytes(bytes([0x5a]) * (2048 * 512))
        vorherigElementeintrag = hashlib.sha256(andererMedien.read_bytes()).hexdigest()
        maschine = VirtuelleMaschine(position / 'build/kernel.elf', speichergerätMittelgroß=andererMedien)
        try:
            maschine.befehl('sync', ['Sync: -19'])
        finally:
            maschine.schließen()
        assert hashlib.sha256(andererMedien.read_bytes()).hexdigest() == vorherigElementeintrag
        ergebnis['foreign_disk_unchanged'] = True
    (position / 'build/Beständigkeitsprüfung.json').write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE ablegenDatenWert/ISO 재부팅/kontrollsumme statuswertWiederherstellen/다른 medienWert 비변경', flush=True)

if __name__ == '__main__':
    befehlAusführen()
