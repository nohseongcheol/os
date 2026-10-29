#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import ভাৰ্ছুৱেল_মেচিন

অৱস্থান = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', অৱস্থান / 'সঁজুলিসমূহ/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def সম্পাদনা_মান(মেচিন, সামগ্ৰী_মান):
    সঞ্চালন = len(মেচিন.লগ_শাৰী)
    মেচিন.직렬.sendall(('edit note.txt\n' + সামগ্ৰী_মান + '\n.save\n').encode())
    return মেচিন.기다림('jkoros> ', সঞ্চালন)

def নিষ্পাদন_আদেশ():
    পৰিমাপ = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.ক্ৰিয়েট_প্রবিষ্ট(매체)
        মেচিন = ভাৰ্ছুৱেল_মেচিন(অৱস্থান / 'build/kernel.elf', 저장매체=매체)
        try:
            মেচিন.কমান্ড('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            সম্পাদনা_মান(মেচিন, 'generation-one')
            মেচিন.কমান্ড('sync', ['Sync: 0'])
            সম্পাদনা_মান(মেচিন, 'generation-two')
            মেচিন.কমান্ড('sync', ['Sync: 0'])
            সম্পাদনা_মান(মেচিন, 'unsynced-three')
            পৰিমাপ['save'] = মেচিন.লগ_শাৰী.decode('utf-8', 'replace')
        finally:
            মেচিন.বন্ধ_কৰক()
        মেচিন = ভাৰ্ছুৱেল_মেচিন(অৱস্থান / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            নিৰ্গম = মেচিন.কমান্ড('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in নিৰ্গম
            মেচিন.কমান্ড('cat stored.txt', ['saved-from-C'])
            পৰিমাপ['restore'] = মেচিন.লগ_শাৰী.decode('utf-8', 'replace')
        finally:
            মেচিন.বন্ধ_কৰক()
        ডাটা = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', ডাটা, (1 + ইনডেক্স * 259) * 512 + 4)[0] for ইনডেক্স in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ডাটা[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(ডাটা)
        মেচিন = ভাৰ্ছুৱেল_মেচিন(অৱস্থান / 'build/kernel.elf', 저장매체=매체)
        try:
            মেচিন.কমান্ড('cat note.txt', ['generation-one'])
            মেচিন.কমান্ড('cat stored.txt', ['saved-from-C'])
            পৰিমাপ['checksum_fallback'] = মেচিন.লগ_শাৰী.decode('utf-8', 'replace')
        finally:
            মেচিন.বন্ধ_কৰক()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        মেচিন = ভাৰ্ছুৱেল_মেচিন(অৱস্থান / 'build/kernel.elf', 저장매체=다른매체)
        try:
            মেচিন.কমান্ড('sync', ['Sync: -19'])
        finally:
            মেচিন.বন্ধ_কৰক()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        পৰিমাপ['foreign_disk_unchanged'] = True
    (অৱস্থান / 'build/보존시험.json').write_text(json.dumps(পৰিমাপ, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE জমা_কৰক_মান/ISO 재부팅/검사합 পুনৰুদ্ধাৰ_কৰক_অৱস্থা/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    নিষ্পাদন_আদেশ()
