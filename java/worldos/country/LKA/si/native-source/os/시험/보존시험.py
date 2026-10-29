#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import අතථ්_ය_යන්ත්_රය

පිහිටීම = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', පිහිටීම / 'මෙවලම්/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def සකසන්න_අගය(යන්ත්_රය, අන්තර්ගතය_අගය):
    ක්_රියාත්මක_කරන්න_2 = len(යන්ත්_රය.ලොගය_පේළිය)
    යන්ත්_රය.직렬.sendall(('edit note.txt\n' + අන්තර්ගතය_අගය + '\n.save\n').encode())
    return යන්ත්_රය.기다림('jkoros> ', ක්_රියාත්මක_කරන්න_2)

def ක්_රියාත්මක_කරන්න_විධානය():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.සාදන්න_පිවිසුම(매체)
        යන්ත්_රය = අතථ්_ය_යන්ත්_රය(පිහිටීම / 'build/kernel.elf', 저장매체=매체)
        try:
            යන්ත්_රය.විධානය('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            සකසන්න_අගය(යන්ත්_රය, 'generation-one')
            යන්ත්_රය.විධානය('sync', ['Sync: 0'])
            සකසන්න_අගය(යන්ත්_රය, 'generation-two')
            යන්ත්_රය.විධානය('sync', ['Sync: 0'])
            සකසන්න_අගය(යන්ත්_රය, 'unsynced-three')
            결과['save'] = යන්ත්_රය.ලොගය_පේළිය.decode('utf-8', 'replace')
        finally:
            යන්ත්_රය.වසන්න()
        යන්ත්_රය = අතථ්_ය_යන්ත්_රය(පිහිටීම / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = යන්ත්_රය.විධානය('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            යන්ත්_රය.විධානය('cat stored.txt', ['saved-from-C'])
            결과['restore'] = යන්ත්_රය.ලොගය_පේළිය.decode('utf-8', 'replace')
        finally:
            යන්ත්_රය.වසන්න()
        දත්ත = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', දත්ත, (1 + සූචිය * 259) * 512 + 4)[0] for සූචිය in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        දත්ත[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(දත්ත)
        යන්ත්_රය = අතථ්_ය_යන්ත්_රය(පිහිටීම / 'build/kernel.elf', 저장매체=매체)
        try:
            යන්ත්_රය.විධානය('cat note.txt', ['generation-one'])
            යන්ත්_රය.විධානය('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = යන්ත්_රය.ලොගය_පේළිය.decode('utf-8', 'replace')
        finally:
            යන්ත්_රය.වසන්න()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        යන්ත්_රය = අතථ්_ය_යන්ත්_රය(පිහිටීම / 'build/kernel.elf', 저장매체=다른매체)
        try:
            යන්ත්_රය.විධානය('sync', ['Sync: -19'])
        finally:
            යන්ත්_රය.වසන්න()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (පිහිටීම / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE ගබඩා_කරන්න_අගය/ISO 재부팅/검사합 නැවත_ලබාගන්න_තත්වය/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_විධානය()
