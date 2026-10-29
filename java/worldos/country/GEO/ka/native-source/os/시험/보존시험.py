#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import ვირტუალური_კომპიუტერი

პოზიცია = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', პოზიცია / 'ხელსაწყოები/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def რედაქტირება_მნიშვნელობა(კომპიუტერი, შიგთავსი_მნიშვნელობა):
    გაშვება = len(კომპიუტერი.ჟურნალი_ჩაწერა)
    კომპიუტერი.직렬.sendall(('edit note.txt\n' + შიგთავსი_მნიშვნელობა + '\n.save\n').encode())
    return კომპიუტერი.მოლოდინი_სტატუსი('jkoros> ', გაშვება)

def შესრულება_ბრძანება():
    გაზომვა = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.შექმნა_შენატანი(매체)
        კომპიუტერი = ვირტუალური_კომპიუტერი(პოზიცია / 'build/kernel.elf', 저장매체=매체)
        try:
            კომპიუტერი.ბრძანება('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            რედაქტირება_მნიშვნელობა(კომპიუტერი, 'generation-one')
            კომპიუტერი.ბრძანება('sync', ['Sync: 0'])
            რედაქტირება_მნიშვნელობა(კომპიუტერი, 'generation-two')
            კომპიუტერი.ბრძანება('sync', ['Sync: 0'])
            რედაქტირება_მნიშვნელობა(კომპიუტერი, 'unsynced-three')
            გაზომვა['save'] = კომპიუტერი.ჟურნალი_ჩაწერა.decode('utf-8', 'replace')
        finally:
            კომპიუტერი.დახურვა()
        კომპიუტერი = ვირტუალური_კომპიუტერი(პოზიცია / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = კომპიუტერი.ბრძანება('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            კომპიუტერი.ბრძანება('cat stored.txt', ['saved-from-C'])
            გაზომვა['restore'] = კომპიუტერი.ჟურნალი_ჩაწერა.decode('utf-8', 'replace')
        finally:
            კომპიუტერი.დახურვა()
        მონაცემები = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', მონაცემები, (1 + ინდექსი * 259) * 512 + 4)[0] for ინდექსი in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        მონაცემები[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(მონაცემები)
        კომპიუტერი = ვირტუალური_კომპიუტერი(პოზიცია / 'build/kernel.elf', 저장매체=매체)
        try:
            კომპიუტერი.ბრძანება('cat note.txt', ['generation-one'])
            კომპიუტერი.ბრძანება('cat stored.txt', ['saved-from-C'])
            გაზომვა['checksum_fallback'] = კომპიუტერი.ჟურნალი_ჩაწერა.decode('utf-8', 'replace')
        finally:
            კომპიუტერი.დახურვა()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        კომპიუტერი = ვირტუალური_კომპიუტერი(პოზიცია / 'build/kernel.elf', 저장매체=다른매체)
        try:
            კომპიუტერი.ბრძანება('sync', ['Sync: -19'])
        finally:
            კომპიუტერი.დახურვა()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        გაზომვა['foreign_disk_unchanged'] = True
    (პოზიცია / 'build/보존시험.json').write_text(json.dumps(გაზომვა, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE შენახვა_მნიშვნელობა/ISO 재부팅/검사합 აღდგენა_სტატუსი/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    შესრულება_ბრძანება()
