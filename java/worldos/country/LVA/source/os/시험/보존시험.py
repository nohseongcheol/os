#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import VM

Novietojums = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('datu_nesējs_rīks', Novietojums / 'Rīki/atvērt_Krātuve_datu_nesējs.py')
datu_nesējs_rīks = importlib.util.module_from_spec(명세)
명세.loader.exec_module(datu_nesējs_rīks)

def Rediģēt_VALUE(mašīna, Saturs_VALUE):
    Palaist = len(mašīna.LOG_RECORD)
    mašīna.직렬.sendall(('edit note.txt\n' + Saturs_VALUE + '\n.save\n').encode())
    return mašīna.nogaides_stāvoklis('jkoros> ', Palaist)

def Izpildīt_komanda():
    mērs = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        datu_nesējs_VALUE = Path(임시) / 'files.img'
        datu_nesējs_rīks.atvērt_ievade(datu_nesējs_VALUE)
        mašīna = VM(Novietojums / 'build/kernel.elf', Krātuve_vide=datu_nesējs_VALUE)
        try:
            mašīna.Komanda('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Rediģēt_VALUE(mašīna, 'generation-one')
            mašīna.Komanda('sync', ['Sync: 0'])
            Rediģēt_VALUE(mašīna, 'generation-two')
            mašīna.Komanda('sync', ['Sync: 0'])
            Rediģēt_VALUE(mašīna, 'unsynced-three')
            mērs['save'] = mašīna.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mašīna.Aizvērt()
        mašīna = VM(Novietojums / 'build/kernel.iso', 'iso', Krātuve_vide=datu_nesējs_VALUE)
        try:
            Izvade = mašīna.Komanda('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Izvade
            mašīna.Komanda('cat stored.txt', ['saved-from-C'])
            mērs['restore'] = mašīna.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mašīna.Aizvērt()
        dati = bytearray(datu_nesējs_VALUE.read_bytes())
        세대들 = [struct.unpack_from('<I', dati, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        dati[(1 + 최신 * 259 + 3) * 512] ^= 1
        datu_nesējs_VALUE.write_bytes(dati)
        mašīna = VM(Novietojums / 'build/kernel.elf', Krātuve_vide=datu_nesējs_VALUE)
        try:
            mašīna.Komanda('cat note.txt', ['generation-one'])
            mašīna.Komanda('cat stored.txt', ['saved-from-C'])
            mērs['checksum_fallback'] = mašīna.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mašīna.Aizvērt()
        Citi_datu_nesējs = Path(임시) / 'foreign.img'
        Citi_datu_nesējs.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(Citi_datu_nesējs.read_bytes()).hexdigest()
        mašīna = VM(Novietojums / 'build/kernel.elf', Krātuve_vide=Citi_datu_nesējs)
        try:
            mašīna.Komanda('sync', ['Sync: -19'])
        finally:
            mašīna.Aizvērt()
        assert hashlib.sha256(Citi_datu_nesējs.read_bytes()).hexdigest() == 이전
        mērs['foreign_disk_unchanged'] = True
    (Novietojums / 'build/보존시험.json').write_text(json.dumps(mērs, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/kontrolsumma atgūt_Statuss/다른 datu_nesējs_VALUE 비변경', flush=True)

if __name__ == '__main__':
    Izpildīt_komanda()
