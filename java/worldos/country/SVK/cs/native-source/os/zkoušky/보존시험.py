#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from test_uživatel_síť import virtuální_počítač

pozice = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('média_nástroj', pozice / 'nástroje/Create_médium.py')
média_nástroj = importlib.util.module_from_spec(명세)
명세.loader.exec_module(média_nástroj)

def úprava_HODNOTA(počítač, Obsah_HODNOTA):
    Spustit_2 = len(počítač.LOGZ_ZÁZNAM)
    počítač.직렬.sendall(('edit note.txt\n' + Obsah_HODNOTA + '\n.save\n').encode())
    return počítač.čekací_stav('jkoros> ', Spustit_2)

def Provést_příkaz():
    VÝSLEDEK = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        média_HODNOTA = Path(임시) / 'files.img'
        média_nástroj.Create_položka(média_HODNOTA)
        počítač = virtuální_počítač(pozice / 'build/kernel.elf', Storage_médium=média_HODNOTA)
        try:
            počítač.příkaz('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            úprava_HODNOTA(počítač, 'generation-one')
            počítač.příkaz('sync', ['Sync: 0'])
            úprava_HODNOTA(počítač, 'generation-two')
            počítač.příkaz('sync', ['Sync: 0'])
            úprava_HODNOTA(počítač, 'unsynced-three')
            VÝSLEDEK['save'] = počítač.LOGZ_ZÁZNAM.decode('utf-8', 'replace')
        finally:
            počítač.Zavřené()
        počítač = virtuální_počítač(pozice / 'build/kernel.iso', 'iso', Storage_médium=média_HODNOTA)
        try:
            výstupní_pozice = počítač.příkaz('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in výstupní_pozice
            počítač.příkaz('cat stored.txt', ['saved-from-C'])
            VÝSLEDEK['restore'] = počítač.LOGZ_ZÁZNAM.decode('utf-8', 'replace')
        finally:
            počítač.Zavřené()
        data = bytearray(média_HODNOTA.read_bytes())
        세대들 = [struct.unpack_from('<I', data, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        data[(1 + 최신 * 259 + 3) * 512] ^= 1
        média_HODNOTA.write_bytes(data)
        počítač = virtuální_počítač(pozice / 'build/kernel.elf', Storage_médium=média_HODNOTA)
        try:
            počítač.příkaz('cat note.txt', ['generation-one'])
            počítač.příkaz('cat stored.txt', ['saved-from-C'])
            VÝSLEDEK['checksum_fallback'] = počítač.LOGZ_ZÁZNAM.decode('utf-8', 'replace')
        finally:
            počítač.Zavřené()
        Jiný_média = Path(임시) / 'foreign.img'
        Jiný_média.write_bytes(bytes([0x5a]) * (2048 * 512))
        Předchozí_zboží = hashlib.sha256(Jiný_média.read_bytes()).hexdigest()
        počítač = virtuální_počítač(pozice / 'build/kernel.elf', Storage_médium=Jiný_média)
        try:
            počítač.příkaz('sync', ['Sync: -19'])
        finally:
            počítač.Zavřené()
        assert hashlib.sha256(Jiný_média.read_bytes()).hexdigest() == Předchozí_zboží
        VÝSLEDEK['foreign_disk_unchanged'] = True
    (pozice / 'build/보존시험.json').write_text(json.dumps(VÝSLEDEK, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_HODNOTA/ISO 재부팅/kontrolní_součet zotavit_Stav/다른 média_HODNOTA 비변경', flush=True)

if __name__ == '__main__':
    Provést_příkaz()
