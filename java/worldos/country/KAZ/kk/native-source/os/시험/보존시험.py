#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import виртуалды_машина

Орны = Path(__file__).resolve().parents[1]
сипаттама = importlib.util.spec_from_file_location('매체도구', Орны / 'Құралдар/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(сипаттама)
сипаттама.loader.exec_module(매체도구)

def өңдеу_мән(компьютер, мазмұн_мән):
    Орындау_2 = len(компьютер.журнал_жол)
    компьютер.직렬.sendall(('edit note.txt\n' + мазмұн_мән + '\n.save\n').encode())
    return компьютер.күту_күйі('jkoros> ', Орындау_2)

def орындау_пәрмен():
    НӘТИЖЕ = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.жасау_енгізу(매체)
        компьютер = виртуалды_машина(Орны / 'build/kernel.elf', 저장매체=매체)
        try:
            компьютер.Команда('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            өңдеу_мән(компьютер, 'generation-one')
            компьютер.Команда('sync', ['Sync: 0'])
            өңдеу_мән(компьютер, 'generation-two')
            компьютер.Команда('sync', ['Sync: 0'])
            өңдеу_мән(компьютер, 'unsynced-three')
            НӘТИЖЕ['save'] = компьютер.журнал_жол.decode('utf-8', 'replace')
        finally:
            компьютер.Жабу()
        компьютер = виртуалды_машина(Орны / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            Шығысы = компьютер.Команда('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Шығысы
            компьютер.Команда('cat stored.txt', ['saved-from-C'])
            НӘТИЖЕ['restore'] = компьютер.журнал_жол.decode('utf-8', 'replace')
        finally:
            компьютер.Жабу()
        деректер = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', деректер, (1 + индекс * 259) * 512 + 4)[0] for индекс in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        деректер[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(деректер)
        компьютер = виртуалды_машина(Орны / 'build/kernel.elf', 저장매체=매체)
        try:
            компьютер.Команда('cat note.txt', ['generation-one'])
            компьютер.Команда('cat stored.txt', ['saved-from-C'])
            НӘТИЖЕ['checksum_fallback'] = компьютер.журнал_жол.decode('utf-8', 'replace')
        finally:
            компьютер.Жабу()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        компьютер = виртуалды_машина(Орны / 'build/kernel.elf', 저장매체=다른매체)
        try:
            компьютер.Команда('sync', ['Sync: -19'])
        finally:
            компьютер.Жабу()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        НӘТИЖЕ['foreign_disk_unchanged'] = True
    (Орны / 'build/보존시험.json').write_text(json.dumps(НӘТИЖЕ, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE сақтау_мән/ISO 재부팅/тексеру_қорытындысы қалпына_келу_күй/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    орындау_пәрмен()
