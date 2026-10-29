#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import sýndar_vél

Staðsetning = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', Staðsetning / 'Verkfæri/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def breyta_VALUE(vél, Efni_VALUE):
    Keyra_2 = len(vél.LOG_lína)
    vél.직렬.sendall(('edit note.txt\n' + Efni_VALUE + '\n.save\n').encode())
    return vél.Bíddu_staða('jkoros> ', Keyra_2)

def keyra_skipun():
    NIÐURSTAÐA = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.stofna_færsla(매체)
        vél = sýndar_vél(Staðsetning / 'build/kernel.elf', 저장매체=매체)
        try:
            vél.Skipun('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            breyta_VALUE(vél, 'generation-one')
            vél.Skipun('sync', ['Sync: 0'])
            breyta_VALUE(vél, 'generation-two')
            vél.Skipun('sync', ['Sync: 0'])
            breyta_VALUE(vél, 'unsynced-three')
            NIÐURSTAÐA['save'] = vél.LOG_lína.decode('utf-8', 'replace')
        finally:
            vél.Loka()
        vél = sýndar_vél(Staðsetning / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            úttak = vél.Skipun('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in úttak
            vél.Skipun('cat stored.txt', ['saved-from-C'])
            NIÐURSTAÐA['restore'] = vél.LOG_lína.decode('utf-8', 'replace')
        finally:
            vél.Loka()
        gögn = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', gögn, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        gögn[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(gögn)
        vél = sýndar_vél(Staðsetning / 'build/kernel.elf', 저장매체=매체)
        try:
            vél.Skipun('cat note.txt', ['generation-one'])
            vél.Skipun('cat stored.txt', ['saved-from-C'])
            NIÐURSTAÐA['checksum_fallback'] = vél.LOG_lína.decode('utf-8', 'replace')
        finally:
            vél.Loka()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        vél = sýndar_vél(Staðsetning / 'build/kernel.elf', 저장매체=다른매체)
        try:
            vél.Skipun('sync', ['Sync: -19'])
        finally:
            vél.Loka()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        NIÐURSTAÐA['foreign_disk_unchanged'] = True
    (Staðsetning / 'build/보존시험.json').write_text(json.dumps(NIÐURSTAÐA, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/prófsumma endurheimta_staða/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    keyra_skipun()
