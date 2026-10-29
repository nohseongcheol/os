#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from testi_käyttäjä_verkko import VM

paikka = Path(__file__).resolve().parents[1]
määritys = importlib.util.spec_from_file_location('tietoväline_työkalu', paikka / 'työkalut/Luo_Tallennus_tietoväline.py')
tietoväline_työkalu = importlib.util.module_from_spec(määritys)
määritys.loader.exec_module(tietoväline_työkalu)

def muutos_ARVO(kone, Sisältö_ARVO):
    Suorita_2 = len(kone.LOG_TIETUE)
    kone.직렬.sendall(('edit note.txt\n' + Sisältö_ARVO + '\n.save\n').encode())
    return kone.odotustila('jkoros> ', Suorita_2)

def Suorita_komento():
    TULOS = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        tietoväline_ARVO = Path(임시) / 'files.img'
        tietoväline_työkalu.Luo_merkintä(tietoväline_ARVO)
        kone = VM(paikka / 'build/kernel.elf', Tallennus_väline=tietoväline_ARVO)
        try:
            kone.komento('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            muutos_ARVO(kone, 'generation-one')
            kone.komento('sync', ['Sync: 0'])
            muutos_ARVO(kone, 'generation-two')
            kone.komento('sync', ['Sync: 0'])
            muutos_ARVO(kone, 'unsynced-three')
            TULOS['save'] = kone.LOG_TIETUE.decode('utf-8', 'replace')
        finally:
            kone.Sulje()
        kone = VM(paikka / 'build/kernel.iso', 'iso', Tallennus_väline=tietoväline_ARVO)
        try:
            tulostuspaikka = kone.komento('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in tulostuspaikka
            kone.komento('cat stored.txt', ['saved-from-C'])
            TULOS['restore'] = kone.LOG_TIETUE.decode('utf-8', 'replace')
        finally:
            kone.Sulje()
        data = bytearray(tietoväline_ARVO.read_bytes())
        세대들 = [struct.unpack_from('<I', data, (1 + INDEKSI * 259) * 512 + 4)[0] for INDEKSI in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        data[(1 + 최신 * 259 + 3) * 512] ^= 1
        tietoväline_ARVO.write_bytes(data)
        kone = VM(paikka / 'build/kernel.elf', Tallennus_väline=tietoväline_ARVO)
        try:
            kone.komento('cat note.txt', ['generation-one'])
            kone.komento('cat stored.txt', ['saved-from-C'])
            TULOS['checksum_fallback'] = kone.LOG_TIETUE.decode('utf-8', 'replace')
        finally:
            kone.Sulje()
        muut_tietoväline = Path(임시) / 'foreign.img'
        muut_tietoväline.write_bytes(bytes([0x5a]) * (2048 * 512))
        Edellinen_kohde = hashlib.sha256(muut_tietoväline.read_bytes()).hexdigest()
        kone = VM(paikka / 'build/kernel.elf', Tallennus_väline=muut_tietoväline)
        try:
            kone.komento('sync', ['Sync: -19'])
        finally:
            kone.Sulje()
        assert hashlib.sha256(muut_tietoväline.read_bytes()).hexdigest() == Edellinen_kohde
        TULOS['foreign_disk_unchanged'] = True
    (paikka / 'build/보존시험.json').write_text(json.dumps(TULOS, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_ARVO/ISO 재부팅/tarkistussumma pelastaa_Tila/다른 tietoväline_ARVO 비변경', flush=True)

if __name__ == '__main__':
    Suorita_komento()
