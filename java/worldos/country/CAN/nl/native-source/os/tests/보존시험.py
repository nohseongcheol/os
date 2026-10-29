#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from test_gebruiker_net import VM

positie = Path(__file__).resolve().parents[1]
specificatie = importlib.util.spec_from_file_location('Media_hulpmiddel', positie / 'hulpmiddelen/maken_Opslag_Media.py')
Media_hulpmiddel = importlib.util.module_from_spec(specificatie)
specificatie.loader.exec_module(Media_hulpmiddel)

def Bewerk_WAARDE(machine, Inhoud_WAARDE):
    starten = len(machine.LOG_RECORD)
    machine.직렬.sendall(('edit note.txt\n' + Inhoud_WAARDE + '\n.save\n').encode())
    return machine.wachtstatus('jkoros> ', starten)

def Uitvoeren_opdracht():
    resultaat = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        Media_WAARDE = Path(임시) / 'files.img'
        Media_hulpmiddel.maken_invoer(Media_WAARDE)
        machine = VM(positie / 'build/kernel.elf', Opslag_medium=Media_WAARDE)
        try:
            machine.opdracht('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Bewerk_WAARDE(machine, 'generation-one')
            machine.opdracht('sync', ['Sync: 0'])
            Bewerk_WAARDE(machine, 'generation-two')
            machine.opdracht('sync', ['Sync: 0'])
            Bewerk_WAARDE(machine, 'unsynced-three')
            resultaat['save'] = machine.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            machine.Sluiten()
        machine = VM(positie / 'build/kernel.iso', 'iso', Opslag_medium=Media_WAARDE)
        try:
            tekstuitvoer = machine.opdracht('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in tekstuitvoer
            machine.opdracht('cat stored.txt', ['saved-from-C'])
            resultaat['restore'] = machine.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            machine.Sluiten()
        gegevens = bytearray(Media_WAARDE.read_bytes())
        세대들 = [struct.unpack_from('<I', gegevens, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        gegevens[(1 + 최신 * 259 + 3) * 512] ^= 1
        Media_WAARDE.write_bytes(gegevens)
        machine = VM(positie / 'build/kernel.elf', Opslag_medium=Media_WAARDE)
        try:
            machine.opdracht('cat note.txt', ['generation-one'])
            machine.opdracht('cat stored.txt', ['saved-from-C'])
            resultaat['checksum_fallback'] = machine.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            machine.Sluiten()
        Overige_Media = Path(임시) / 'foreign.img'
        Overige_Media.write_bytes(bytes([0x5a]) * (2048 * 512))
        Vorige_item = hashlib.sha256(Overige_Media.read_bytes()).hexdigest()
        machine = VM(positie / 'build/kernel.elf', Opslag_medium=Overige_Media)
        try:
            machine.opdracht('sync', ['Sync: -19'])
        finally:
            machine.Sluiten()
        assert hashlib.sha256(Overige_Media.read_bytes()).hexdigest() == Vorige_item
        resultaat['foreign_disk_unchanged'] = True
    (positie / 'build/보존시험.json').write_text(json.dumps(resultaat, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_WAARDE/ISO 재부팅/controlesom herstellen_Status/다른 Media_WAARDE 비변경', flush=True)

if __name__ == '__main__':
    Uitvoeren_opdracht()
