#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import কল্পিত_মেশিন

অবস্থান = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', অবস্থান / 'সরঞ্জামগুলি/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def সম্পাদন_মান(মেশিন, সামগ্রি_মান):
    চালনা = len(মেশিন.লগ_সারি)
    মেশিন.직렬.sendall(('edit note.txt\n' + সামগ্রি_মান + '\n.save\n').encode())
    return মেশিন.অপেক্ষা_অবস্হা('jkoros> ', চালনা)

def কার্যকর_করুন_আদেশ():
    পরিমাপ = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.ক্রিয়েট_ভুক্তি(매체)
        মেশিন = কল্পিত_মেশিন(অবস্থান / 'build/kernel.elf', 저장매체=매체)
        try:
            মেশিন.আদেশ('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            সম্পাদন_মান(মেশিন, 'generation-one')
            মেশিন.আদেশ('sync', ['Sync: 0'])
            সম্পাদন_মান(মেশিন, 'generation-two')
            মেশিন.আদেশ('sync', ['Sync: 0'])
            সম্পাদন_মান(মেশিন, 'unsynced-three')
            পরিমাপ['save'] = মেশিন.লগ_সারি.decode('utf-8', 'replace')
        finally:
            মেশিন.বন্ধ_করুন()
        মেশিন = কল্পিত_মেশিন(অবস্থান / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            নির্গম = মেশিন.আদেশ('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in নির্গম
            মেশিন.আদেশ('cat stored.txt', ['saved-from-C'])
            পরিমাপ['restore'] = মেশিন.লগ_সারি.decode('utf-8', 'replace')
        finally:
            মেশিন.বন্ধ_করুন()
        ডাটা = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', ডাটা, (1 + সূচি * 259) * 512 + 4)[0] for সূচি in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ডাটা[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(ডাটা)
        মেশিন = কল্পিত_মেশিন(অবস্থান / 'build/kernel.elf', 저장매체=매체)
        try:
            মেশিন.আদেশ('cat note.txt', ['generation-one'])
            মেশিন.আদেশ('cat stored.txt', ['saved-from-C'])
            পরিমাপ['checksum_fallback'] = মেশিন.লগ_সারি.decode('utf-8', 'replace')
        finally:
            মেশিন.বন্ধ_করুন()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        মেশিন = কল্পিত_মেশিন(অবস্থান / 'build/kernel.elf', 저장매체=다른매체)
        try:
            মেশিন.আদেশ('sync', ['Sync: -19'])
        finally:
            মেশিন.বন্ধ_করুন()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        পরিমাপ['foreign_disk_unchanged'] = True
    (অবস্থান / 'build/보존시험.json').write_text(json.dumps(পরিমাপ, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE ভাণ্ডার_মান/ISO 재부팅/চেকসাম পুনরুদ্ধার_অবস্হা/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    কার্যকর_করুন_আদেশ()
