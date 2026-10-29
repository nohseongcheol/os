#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from test_používateľ_sieť import virtuálny_počítač

Pozícia = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('médiá_nástroj', Pozícia / 'Nástroje/Create_Úložisko_médiá.py')
médiá_nástroj = importlib.util.module_from_spec(명세)
명세.loader.exec_module(médiá_nástroj)

def úprava_VALUE(počítač_5eb260fa, obsah_VALUE):
    Spustiť_2 = len(počítač_5eb260fa.LOG_RECORD)
    počítač_5eb260fa.직렬.sendall(('edit note.txt\n' + obsah_VALUE + '\n.save\n').encode())
    return počítač_5eb260fa.stav_čakania('jkoros> ', Spustiť_2)

def Vykonať_príkaz():
    KR = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        médiá_VALUE = Path(임시) / 'files.img'
        médiá_nástroj.Create_položka(médiá_VALUE)
        počítač_5eb260fa = virtuálny_počítač(Pozícia / 'build/kernel.elf', Úložisko_médium=médiá_VALUE)
        try:
            počítač_5eb260fa.Príkaz('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            úprava_VALUE(počítač_5eb260fa, 'generation-one')
            počítač_5eb260fa.Príkaz('sync', ['Sync: 0'])
            úprava_VALUE(počítač_5eb260fa, 'generation-two')
            počítač_5eb260fa.Príkaz('sync', ['Sync: 0'])
            úprava_VALUE(počítač_5eb260fa, 'unsynced-three')
            KR['save'] = počítač_5eb260fa.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            počítač_5eb260fa.Zatvoriť()
        počítač_5eb260fa = virtuálny_počítač(Pozícia / 'build/kernel.iso', 'iso', Úložisko_médium=médiá_VALUE)
        try:
            Výstup = počítač_5eb260fa.Príkaz('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Výstup
            počítač_5eb260fa.Príkaz('cat stored.txt', ['saved-from-C'])
            KR['restore'] = počítač_5eb260fa.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            počítač_5eb260fa.Zatvoriť()
        údaje = bytearray(médiá_VALUE.read_bytes())
        세대들 = [struct.unpack_from('<I', údaje, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        údaje[(1 + 최신 * 259 + 3) * 512] ^= 1
        médiá_VALUE.write_bytes(údaje)
        počítač_5eb260fa = virtuálny_počítač(Pozícia / 'build/kernel.elf', Úložisko_médium=médiá_VALUE)
        try:
            počítač_5eb260fa.Príkaz('cat note.txt', ['generation-one'])
            počítač_5eb260fa.Príkaz('cat stored.txt', ['saved-from-C'])
            KR['checksum_fallback'] = počítač_5eb260fa.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            počítač_5eb260fa.Zatvoriť()
        Iné_médiá = Path(임시) / 'foreign.img'
        Iné_médiá.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(Iné_médiá.read_bytes()).hexdigest()
        počítač_5eb260fa = virtuálny_počítač(Pozícia / 'build/kernel.elf', Úložisko_médium=Iné_médiá)
        try:
            počítač_5eb260fa.Príkaz('sync', ['Sync: -19'])
        finally:
            počítač_5eb260fa.Zatvoriť()
        assert hashlib.sha256(Iné_médiá.read_bytes()).hexdigest() == 이전
        KR['foreign_disk_unchanged'] = True
    (Pozícia / 'build/보존시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/kontrolný_súčet obnoviť_Stav/다른 médiá_VALUE 비변경', flush=True)

if __name__ == '__main__':
    Vykonať_príkaz()
