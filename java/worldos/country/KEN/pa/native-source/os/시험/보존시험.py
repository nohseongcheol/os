#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import ਵਰਚੁਅਲ_ਮਸ਼ੀਨ

ਸਥਿਤੀ = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', ਸਥਿਤੀ / 'ਸਾਧਨ/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, ਤਤਕਰਾ_ਕੀਮਤ):
    ਚਲਾਓ_2 = len(ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ)
    ਮਸ਼ੀਨ.직렬.sendall(('edit note.txt\n' + ਤਤਕਰਾ_ਕੀਮਤ + '\n.save\n').encode())
    return ਮਸ਼ੀਨ.기다림('jkoros> ', ਚਲਾਓ_2)

def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼():
    ਮਾਪ = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.ਬਣਾਓ_ਦਾਖਲਾ(매체)
        ਮਸ਼ੀਨ = ਵਰਚੁਅਲ_ਮਸ਼ੀਨ(ਸਥਿਤੀ / 'build/kernel.elf', 저장매체=매체)
        try:
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, 'generation-one')
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('sync', ['Sync: 0'])
            ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, 'generation-two')
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('sync', ['Sync: 0'])
            ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, 'unsynced-three')
            ਮਾਪ['save'] = ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ.decode('utf-8', 'replace')
        finally:
            ਮਸ਼ੀਨ.ਬੰਦ_ਕਰੋ()
        ਮਸ਼ੀਨ = ਵਰਚੁਅਲ_ਮਸ਼ੀਨ(ਸਥਿਤੀ / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            ਆਉਟਪੁੱਟ = ਮਸ਼ੀਨ.ਕਮਾਂਡ('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in ਆਉਟਪੁੱਟ
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('cat stored.txt', ['saved-from-C'])
            ਮਾਪ['restore'] = ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ.decode('utf-8', 'replace')
        finally:
            ਮਸ਼ੀਨ.ਬੰਦ_ਕਰੋ()
        ਸਮੱਗਰੀ = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', ਸਮੱਗਰੀ, (1 + ਅਨੁਕ੍ਰਮਣਿਕਾ * 259) * 512 + 4)[0] for ਅਨੁਕ੍ਰਮਣਿਕਾ in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ਸਮੱਗਰੀ[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(ਸਮੱਗਰੀ)
        ਮਸ਼ੀਨ = ਵਰਚੁਅਲ_ਮਸ਼ੀਨ(ਸਥਿਤੀ / 'build/kernel.elf', 저장매체=매체)
        try:
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('cat note.txt', ['generation-one'])
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('cat stored.txt', ['saved-from-C'])
            ਮਾਪ['checksum_fallback'] = ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ.decode('utf-8', 'replace')
        finally:
            ਮਸ਼ੀਨ.ਬੰਦ_ਕਰੋ()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        ਮਸ਼ੀਨ = ਵਰਚੁਅਲ_ਮਸ਼ੀਨ(ਸਥਿਤੀ / 'build/kernel.elf', 저장매체=다른매체)
        try:
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('sync', ['Sync: -19'])
        finally:
            ਮਸ਼ੀਨ.ਬੰਦ_ਕਰੋ()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        ਮਾਪ['foreign_disk_unchanged'] = True
    (ਸਥਿਤੀ / 'build/보존시험.json').write_text(json.dumps(ਮਾਪ, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE ਸੰਭਾਲੋ_ਕੀਮਤ/ISO 재부팅/검사합 ਮੁੜ_ਪ੍ਰਾਪਤ_ਕਰਨਾ_ਸਥਿਤੀ/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
