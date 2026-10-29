#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import مەجازی_مەکینه

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('میدیا_ئامراز', 위치 / 'ئامرازەکان/دروستکردن_هەمارگە_میدیا.py')
میدیا_ئامراز = importlib.util.module_from_spec(명세)
명세.loader.exec_module(میدیا_ئامراز)

def بژار_نرخ(مەکینه, ناوەرۆک_نرخ):
    ڕادان = len(مەکینه.تۆمار_ڕزن)
    مەکینه.직렬.sendall(('edit note.txt\n' + ناوەرۆک_نرخ + '\n.save\n').encode())
    return مەکینه.چاوەڕوان_کردن_دۆخ('jkoros> ', ڕادان)

def جێبەجێکردن_فەرمان():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        میدیا_نرخ = Path(임시) / 'files.img'
        میدیا_ئامراز.دروستکردن_تێنووسین(میدیا_نرخ)
        مەکینه = مەجازی_مەکینه(위치 / 'build/kernel.elf', 저장매체=میدیا_نرخ)
        try:
            مەکینه.فەرمان('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            بژار_نرخ(مەکینه, 'generation-one')
            مەکینه.فەرمان('sync', ['Sync: 0'])
            بژار_نرخ(مەکینه, 'generation-two')
            مەکینه.فەرمان('sync', ['Sync: 0'])
            بژار_نرخ(مەکینه, 'unsynced-three')
            결과['save'] = مەکینه.تۆمار_ڕزن.decode('utf-8', 'replace')
        finally:
            مەکینه.داخستن()
        مەکینه = مەجازی_مەکینه(위치 / 'build/kernel.iso', 'iso', 저장매체=میدیا_نرخ)
        try:
            출력 = مەکینه.فەرمان('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            مەکینه.فەرمان('cat stored.txt', ['saved-from-C'])
            결과['restore'] = مەکینه.تۆمار_ڕزن.decode('utf-8', 'replace')
        finally:
            مەکینه.داخستن()
        دەیتا = bytearray(میدیا_نرخ.read_bytes())
        세대들 = [struct.unpack_from('<I', دەیتا, (1 + پێرست * 259) * 512 + 4)[0] for پێرست in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        دەیتا[(1 + 최신 * 259 + 3) * 512] ^= 1
        میدیا_نرخ.write_bytes(دەیتا)
        مەکینه = مەجازی_مەکینه(위치 / 'build/kernel.elf', 저장매체=میدیا_نرخ)
        try:
            مەکینه.فەرمان('cat note.txt', ['generation-one'])
            مەکینه.فەرمان('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = مەکینه.تۆمار_ڕزن.decode('utf-8', 'replace')
        finally:
            مەکینه.داخستن()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        مەکینه = مەجازی_مەکینه(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            مەکینه.فەرمان('sync', ['Sync: -19'])
        finally:
            مەکینه.داخستن()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_نرخ/ISO 재부팅/검사합 گەڕاندنەوە_دۆخ/다른 میدیا_نرخ 비변경', flush=True)

if __name__ == '__main__':
    جێبەجێکردن_فەرمان()
