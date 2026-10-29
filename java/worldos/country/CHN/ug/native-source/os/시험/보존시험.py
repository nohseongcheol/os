#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import مەۋھۇم_ماشىنا

ئورۇن = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('مېدىيا_قورال', ئورۇن / 'قوراللار/قۇرۇش_بوشلۇق_مېدىيا.py')
مېدىيا_قورال = importlib.util.module_from_spec(명세)
명세.loader.exec_module(مېدىيا_قورال)

def تەھرىرلەش_قىممىتى(ماشىنا, مەزمۇن_قىممىتى):
    ئىجرا_قىل_2 = len(ماشىنا.خاتىرە_قۇر)
    ماشىنا.직렬.sendall(('edit note.txt\n' + مەزمۇن_قىممىتى + '\n.save\n').encode())
    return ماشىنا.기다림('jkoros> ', ئىجرا_قىل_2)

def ئىجرا_قىلىش_بۇيرۇق():
    ئۆلچەم = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        مېدىيا_قىممىتى = Path(임시) / 'files.img'
        مېدىيا_قورال.قۇرۇش_كىرگۈزۈش(مېدىيا_قىممىتى)
        ماشىنا = مەۋھۇم_ماشىنا(ئورۇن / 'build/kernel.elf', 저장매체=مېدىيا_قىممىتى)
        try:
            ماشىنا.بۇيرۇق('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            تەھرىرلەش_قىممىتى(ماشىنا, 'generation-one')
            ماشىنا.بۇيرۇق('sync', ['Sync: 0'])
            تەھرىرلەش_قىممىتى(ماشىنا, 'generation-two')
            ماشىنا.بۇيرۇق('sync', ['Sync: 0'])
            تەھرىرلەش_قىممىتى(ماشىنا, 'unsynced-three')
            ئۆلچەم['save'] = ماشىنا.خاتىرە_قۇر.decode('utf-8', 'replace')
        finally:
            ماشىنا.ياپ()
        ماشىنا = مەۋھۇم_ماشىنا(ئورۇن / 'build/kernel.iso', 'iso', 저장매체=مېدىيا_قىممىتى)
        try:
            چىقار = ماشىنا.بۇيرۇق('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in چىقار
            ماشىنا.بۇيرۇق('cat stored.txt', ['saved-from-C'])
            ئۆلچەم['restore'] = ماشىنا.خاتىرە_قۇر.decode('utf-8', 'replace')
        finally:
            ماشىنا.ياپ()
        مەلۇمات = bytearray(مېدىيا_قىممىتى.read_bytes())
        세대들 = [struct.unpack_from('<I', مەلۇمات, (1 + ئىندېكس * 259) * 512 + 4)[0] for ئىندېكس in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        مەلۇمات[(1 + 최신 * 259 + 3) * 512] ^= 1
        مېدىيا_قىممىتى.write_bytes(مەلۇمات)
        ماشىنا = مەۋھۇم_ماشىنا(ئورۇن / 'build/kernel.elf', 저장매체=مېدىيا_قىممىتى)
        try:
            ماشىنا.بۇيرۇق('cat note.txt', ['generation-one'])
            ماشىنا.بۇيرۇق('cat stored.txt', ['saved-from-C'])
            ئۆلچەم['checksum_fallback'] = ماشىنا.خاتىرە_قۇر.decode('utf-8', 'replace')
        finally:
            ماشىنا.ياپ()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        ماشىنا = مەۋھۇم_ماشىنا(ئورۇن / 'build/kernel.elf', 저장매체=다른매체)
        try:
            ماشىنا.بۇيرۇق('sync', ['Sync: -19'])
        finally:
            ماشىنا.ياپ()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        ئۆلچەم['foreign_disk_unchanged'] = True
    (ئورۇن / 'build/보존시험.json').write_text(json.dumps(ئۆلچەم, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE ساقلىماق_قىممىتى/ISO 재부팅/검사합 ئەسلىگە_قايتۇرماق_ھالەت/다른 مېدىيا_قىممىتى 비변경', flush=True)

if __name__ == '__main__':
    ئىجرا_قىلىش_بۇيرۇق()
