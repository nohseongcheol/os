#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import தோற்றநிலை_இயந்திரம்

இடம் = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', இடம் / 'கருவிகள்/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def திருத்து_மதிப்பு(இயந்திரம், உள்ளடக்கம்_மதிப்பு):
    செயல்படுத்துக = len(இயந்திரம்.பதிவு_பதிவு)
    இயந்திரம்.직렬.sendall(('edit note.txt\n' + உள்ளடக்கம்_மதிப்பு + '\n.save\n').encode())
    return இயந்திரம்.காத்திரு_நிலை('jkoros> ', செயல்படுத்துக)

def இயக்கு_கட்டளை():
    அளவிடக்கூடியது = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.உருவாக்கு_உள்ளீடு(매체)
        இயந்திரம் = தோற்றநிலை_இயந்திரம்(இடம் / 'build/kernel.elf', 저장매체=매체)
        try:
            இயந்திரம்.கட்டளை('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            திருத்து_மதிப்பு(இயந்திரம், 'generation-one')
            இயந்திரம்.கட்டளை('sync', ['Sync: 0'])
            திருத்து_மதிப்பு(இயந்திரம், 'generation-two')
            இயந்திரம்.கட்டளை('sync', ['Sync: 0'])
            திருத்து_மதிப்பு(இயந்திரம், 'unsynced-three')
            அளவிடக்கூடியது['save'] = இயந்திரம்.பதிவு_பதிவு.decode('utf-8', 'replace')
        finally:
            இயந்திரம்.மூடு()
        இயந்திரம் = தோற்றநிலை_இயந்திரம்(இடம் / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            வெளியீட்டு_இடம் = இயந்திரம்.கட்டளை('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in வெளியீட்டு_இடம்
            இயந்திரம்.கட்டளை('cat stored.txt', ['saved-from-C'])
            அளவிடக்கூடியது['restore'] = இயந்திரம்.பதிவு_பதிவு.decode('utf-8', 'replace')
        finally:
            இயந்திரம்.மூடு()
        தரவு = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', தரவு, (1 + அடைவு * 259) * 512 + 4)[0] for அடைவு in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        தரவு[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(தரவு)
        இயந்திரம் = தோற்றநிலை_இயந்திரம்(இடம் / 'build/kernel.elf', 저장매체=매체)
        try:
            இயந்திரம்.கட்டளை('cat note.txt', ['generation-one'])
            இயந்திரம்.கட்டளை('cat stored.txt', ['saved-from-C'])
            அளவிடக்கூடியது['checksum_fallback'] = இயந்திரம்.பதிவு_பதிவு.decode('utf-8', 'replace')
        finally:
            இயந்திரம்.மூடு()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        இயந்திரம் = தோற்றநிலை_இயந்திரம்(இடம் / 'build/kernel.elf', 저장매체=다른매체)
        try:
            இயந்திரம்.கட்டளை('sync', ['Sync: -19'])
        finally:
            இயந்திரம்.மூடு()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        அளவிடக்கூடியது['foreign_disk_unchanged'] = True
    (இடம் / 'build/보존시험.json').write_text(json.dumps(அளவிடக்கூடியது, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE சேகரி_மதிப்பு/ISO 재부팅/சொதனைக்_கணக்கு மீட்டெடு_நிலை/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    இயக்கு_கட்டளை()
