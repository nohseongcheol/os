#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import VM

pozicija = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', pozicija / 'Alatke/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def Uredi_VALUE(računar, Sadržaj_VALUE):
    koristiti = len(računar.LOG_snimi)
    računar.직렬.sendall(('edit note.txt\n' + Sadržaj_VALUE + '\n.save\n').encode())
    return računar.stanje_čekanja('jkoros> ', koristiti)

def Izvrši_komanda():
    KR = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.Create_stavka(매체)
        računar = VM(pozicija / 'build/kernel.elf', Skladište_Srednja=매체)
        try:
            računar.komanda('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Uredi_VALUE(računar, 'generation-one')
            računar.komanda('sync', ['Sync: 0'])
            Uredi_VALUE(računar, 'generation-two')
            računar.komanda('sync', ['Sync: 0'])
            Uredi_VALUE(računar, 'unsynced-three')
            KR['save'] = računar.LOG_snimi.decode('utf-8', 'replace')
        finally:
            računar.Zatvori()
        računar = VM(pozicija / 'build/kernel.iso', 'iso', Skladište_Srednja=매체)
        try:
            출력 = računar.komanda('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            računar.komanda('cat stored.txt', ['saved-from-C'])
            KR['restore'] = računar.LOG_snimi.decode('utf-8', 'replace')
        finally:
            računar.Zatvori()
        podaci = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', podaci, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        podaci[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(podaci)
        računar = VM(pozicija / 'build/kernel.elf', Skladište_Srednja=매체)
        try:
            računar.komanda('cat note.txt', ['generation-one'])
            računar.komanda('cat stored.txt', ['saved-from-C'])
            KR['checksum_fallback'] = računar.LOG_snimi.decode('utf-8', 'replace')
        finally:
            računar.Zatvori()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        računar = VM(pozicija / 'build/kernel.elf', Skladište_Srednja=다른매체)
        try:
            računar.komanda('sync', ['Sync: -19'])
        finally:
            računar.Zatvori()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        KR['foreign_disk_unchanged'] = True
    (pozicija / 'build/보존시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/kontrolni_zbir oporaviti_Status/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    Izvrši_komanda()
