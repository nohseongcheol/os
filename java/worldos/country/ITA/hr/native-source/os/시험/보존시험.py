#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import VM

Položaj = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('medij_alat', Položaj / 'Alati/Create_Pohrana_medij.py')
medij_alat = importlib.util.module_from_spec(명세)
명세.loader.exec_module(medij_alat)

def Uredi_VALUE(stroj, Sadržaj_VALUE):
    Pokreni = len(stroj.LOG_zapis)
    stroj.직렬.sendall(('edit note.txt\n' + Sadržaj_VALUE + '\n.save\n').encode())
    return stroj.stanje_čekanja('jkoros> ', Pokreni)

def Izvrši_naredba():
    REZULTAT = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        medij_VALUE = Path(임시) / 'files.img'
        medij_alat.Create_unos(medij_VALUE)
        stroj = VM(Položaj / 'build/kernel.elf', Pohrana_medij=medij_VALUE)
        try:
            stroj.Naredba('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Uredi_VALUE(stroj, 'generation-one')
            stroj.Naredba('sync', ['Sync: 0'])
            Uredi_VALUE(stroj, 'generation-two')
            stroj.Naredba('sync', ['Sync: 0'])
            Uredi_VALUE(stroj, 'unsynced-three')
            REZULTAT['save'] = stroj.LOG_zapis.decode('utf-8', 'replace')
        finally:
            stroj.Zatvori()
        stroj = VM(Položaj / 'build/kernel.iso', 'iso', Pohrana_medij=medij_VALUE)
        try:
            Izlaz = stroj.Naredba('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Izlaz
            stroj.Naredba('cat stored.txt', ['saved-from-C'])
            REZULTAT['restore'] = stroj.LOG_zapis.decode('utf-8', 'replace')
        finally:
            stroj.Zatvori()
        podaci = bytearray(medij_VALUE.read_bytes())
        세대들 = [struct.unpack_from('<I', podaci, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        podaci[(1 + 최신 * 259 + 3) * 512] ^= 1
        medij_VALUE.write_bytes(podaci)
        stroj = VM(Položaj / 'build/kernel.elf', Pohrana_medij=medij_VALUE)
        try:
            stroj.Naredba('cat note.txt', ['generation-one'])
            stroj.Naredba('cat stored.txt', ['saved-from-C'])
            REZULTAT['checksum_fallback'] = stroj.LOG_zapis.decode('utf-8', 'replace')
        finally:
            stroj.Zatvori()
        Ostalo_medij = Path(임시) / 'foreign.img'
        Ostalo_medij.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(Ostalo_medij.read_bytes()).hexdigest()
        stroj = VM(Položaj / 'build/kernel.elf', Pohrana_medij=Ostalo_medij)
        try:
            stroj.Naredba('sync', ['Sync: -19'])
        finally:
            stroj.Zatvori()
        assert hashlib.sha256(Ostalo_medij.read_bytes()).hexdigest() == 이전
        REZULTAT['foreign_disk_unchanged'] = True
    (Položaj / 'build/보존시험.json').write_text(json.dumps(REZULTAT, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/kontrolni_zbroj oporaviti_Stanje/다른 medij_VALUE 비변경', flush=True)

if __name__ == '__main__':
    Izvrši_naredba()
