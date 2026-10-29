#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import виртуалдык_машина

Турган_жери = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', Турган_жери / 'Куралдар/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def түзөтүү_маани(машина, Мазмун_маани):
    Жүргүзүү = len(машина.жазуу_катар)
    машина.직렬.sendall(('edit note.txt\n' + Мазмун_маани + '\n.save\n').encode())
    return машина.기다림('jkoros> ', Жүргүзүү)

def аткаруу_буйрук():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.түзүү_киргизме_жазуу(매체)
        машина = виртуалдык_машина(Турган_жери / 'build/kernel.elf', 저장매체=매체)
        try:
            машина.Команда('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            түзөтүү_маани(машина, 'generation-one')
            машина.Команда('sync', ['Sync: 0'])
            түзөтүү_маани(машина, 'generation-two')
            машина.Команда('sync', ['Sync: 0'])
            түзөтүү_маани(машина, 'unsynced-three')
            결과['save'] = машина.жазуу_катар.decode('utf-8', 'replace')
        finally:
            машина.Жабуу()
        машина = виртуалдык_машина(Турган_жери / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            Чыгыш = машина.Команда('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Чыгыш
            машина.Команда('cat stored.txt', ['saved-from-C'])
            결과['restore'] = машина.жазуу_катар.decode('utf-8', 'replace')
        finally:
            машина.Жабуу()
        берилмелер = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', берилмелер, (1 + индекс * 259) * 512 + 4)[0] for индекс in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        берилмелер[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(берилмелер)
        машина = виртуалдык_машина(Турган_жери / 'build/kernel.elf', 저장매체=매체)
        try:
            машина.Команда('cat note.txt', ['generation-one'])
            машина.Команда('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = машина.жазуу_катар.decode('utf-8', 'replace')
        finally:
            машина.Жабуу()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        машина = виртуалдык_машина(Турган_жери / 'build/kernel.elf', 저장매체=다른매체)
        try:
            машина.Команда('sync', ['Sync: -19'])
        finally:
            машина.Жабуу()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (Турган_жери / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE сактагыч_маани/ISO 재부팅/검사합 калыбына_келтирүү_абал/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    аткаруу_буйрук()
