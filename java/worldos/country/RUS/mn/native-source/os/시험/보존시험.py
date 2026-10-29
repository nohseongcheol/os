#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import виртуал_компьютер

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', 위치 / 'Хэрэгслүүд/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def засварлах_утга(компьютер, Агуулга_утга):
    Ажиллуулах = len(компьютер.бичих_мөр_6e8b375a)
    компьютер.직렬.sendall(('edit note.txt\n' + Агуулга_утга + '\n.save\n').encode())
    return компьютер.기다림('jkoros> ', Ажиллуулах)

def Гүйцэтгэх_команд():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.үүсгэх_оролт(매체)
        компьютер = виртуал_компьютер(위치 / 'build/kernel.elf', 저장매체=매체)
        try:
            компьютер.Тушаал('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            засварлах_утга(компьютер, 'generation-one')
            компьютер.Тушаал('sync', ['Sync: 0'])
            засварлах_утга(компьютер, 'generation-two')
            компьютер.Тушаал('sync', ['Sync: 0'])
            засварлах_утга(компьютер, 'unsynced-three')
            결과['save'] = компьютер.бичих_мөр_6e8b375a.decode('utf-8', 'replace')
        finally:
            компьютер.Хаах()
        компьютер = виртуал_компьютер(위치 / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = компьютер.Тушаал('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            компьютер.Тушаал('cat stored.txt', ['saved-from-C'])
            결과['restore'] = компьютер.бичих_мөр_6e8b375a.decode('utf-8', 'replace')
        finally:
            компьютер.Хаах()
        өгөгдөл = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', өгөгдөл, (1 + индекс * 259) * 512 + 4)[0] for индекс in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        өгөгдөл[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(өгөгдөл)
        компьютер = виртуал_компьютер(위치 / 'build/kernel.elf', 저장매체=매체)
        try:
            компьютер.Тушаал('cat note.txt', ['generation-one'])
            компьютер.Тушаал('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = компьютер.бичих_мөр_6e8b375a.decode('utf-8', 'replace')
        finally:
            компьютер.Хаах()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        компьютер = виртуал_компьютер(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            компьютер.Тушаал('sync', ['Sync: -19'])
        finally:
            компьютер.Хаах()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE хадгалах_утга/ISO 재부팅/검사합 сэргээх_төлөв/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    Гүйцэтгэх_команд()
