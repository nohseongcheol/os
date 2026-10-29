#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import VM

Pozicija = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('medija_įrankis', Pozicija / 'Įrankiai/kurti_Saugykla_medija.py')
medija_įrankis = importlib.util.module_from_spec(명세)
명세.loader.exec_module(medija_įrankis)

def redaguoti_VALUE(mašina, Turinys_VALUE):
    Paleisti = len(mašina.LOG_RECORD)
    mašina.직렬.sendall(('edit note.txt\n' + Turinys_VALUE + '\n.save\n').encode())
    return mašina.laukimo_būsena('jkoros> ', Paleisti)

def Vykdyti_komanda():
    REZULTATAS = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        medija_VALUE = Path(임시) / 'files.img'
        medija_įrankis.kurti_įrašas(medija_VALUE)
        mašina = VM(Pozicija / 'build/kernel.elf', Saugykla_terpė=medija_VALUE)
        try:
            mašina.Komanda('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            redaguoti_VALUE(mašina, 'generation-one')
            mašina.Komanda('sync', ['Sync: 0'])
            redaguoti_VALUE(mašina, 'generation-two')
            mašina.Komanda('sync', ['Sync: 0'])
            redaguoti_VALUE(mašina, 'unsynced-three')
            REZULTATAS['save'] = mašina.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mašina.Užverti()
        mašina = VM(Pozicija / 'build/kernel.iso', 'iso', Saugykla_terpė=medija_VALUE)
        try:
            Išvestis = mašina.Komanda('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Išvestis
            mašina.Komanda('cat stored.txt', ['saved-from-C'])
            REZULTATAS['restore'] = mašina.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mašina.Užverti()
        duomenys = bytearray(medija_VALUE.read_bytes())
        세대들 = [struct.unpack_from('<I', duomenys, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        duomenys[(1 + 최신 * 259 + 3) * 512] ^= 1
        medija_VALUE.write_bytes(duomenys)
        mašina = VM(Pozicija / 'build/kernel.elf', Saugykla_terpė=medija_VALUE)
        try:
            mašina.Komanda('cat note.txt', ['generation-one'])
            mašina.Komanda('cat stored.txt', ['saved-from-C'])
            REZULTATAS['checksum_fallback'] = mašina.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mašina.Užverti()
        Kita_medija = Path(임시) / 'foreign.img'
        Kita_medija.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(Kita_medija.read_bytes()).hexdigest()
        mašina = VM(Pozicija / 'build/kernel.elf', Saugykla_terpė=Kita_medija)
        try:
            mašina.Komanda('sync', ['Sync: -19'])
        finally:
            mašina.Užverti()
        assert hashlib.sha256(Kita_medija.read_bytes()).hexdigest() == 이전
        REZULTATAS['foreign_disk_unchanged'] = True
    (Pozicija / 'build/보존시험.json').write_text(json.dumps(REZULTATAS, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/kontrolinė_suma atkurti_Būsena/다른 medija_VALUE 비변경', flush=True)

if __name__ == '__main__':
    Vykdyti_komanda()
