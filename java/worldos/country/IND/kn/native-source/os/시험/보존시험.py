#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import ಅಗೋಚರ_ಯಂತ್ರ

ಸ್ಥಾನ = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', ಸ್ಥಾನ / 'ಪರಿಕರಗಳು/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, ವಿಷಯ_ಮೌಲ್ಯ):
    ಚಲಾಯಿಸು_2 = len(ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ)
    ಯಂತ್ರ.직렬.sendall(('edit note.txt\n' + ವಿಷಯ_ಮೌಲ್ಯ + '\n.save\n').encode())
    return ಯಂತ್ರ.ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ('jkoros> ', ಚಲಾಯಿಸು_2)

def ಪೂರೈಸು_ಆದೇಶ():
    ಮಾಪನ = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.ರಚಿಸು_ನಮೂದು(매체)
        ಯಂತ್ರ = ಅಗೋಚರ_ಯಂತ್ರ(ಸ್ಥಾನ / 'build/kernel.elf', 저장매체=매체)
        try:
            ಯಂತ್ರ.ಆಜ್ಞೆ('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, 'generation-one')
            ಯಂತ್ರ.ಆಜ್ಞೆ('sync', ['Sync: 0'])
            ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, 'generation-two')
            ಯಂತ್ರ.ಆಜ್ಞೆ('sync', ['Sync: 0'])
            ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಯಂತ್ರ, 'unsynced-three')
            ಮಾಪನ['save'] = ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ.decode('utf-8', 'replace')
        finally:
            ಯಂತ್ರ.ಮುಚ್ಚು()
        ಯಂತ್ರ = ಅಗೋಚರ_ಯಂತ್ರ(ಸ್ಥಾನ / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            ಔಟ್_ಪುಟ್ = ಯಂತ್ರ.ಆಜ್ಞೆ('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in ಔಟ್_ಪುಟ್
            ಯಂತ್ರ.ಆಜ್ಞೆ('cat stored.txt', ['saved-from-C'])
            ಮಾಪನ['restore'] = ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ.decode('utf-8', 'replace')
        finally:
            ಯಂತ್ರ.ಮುಚ್ಚು()
        ಡೇಟಾ = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', ಡೇಟಾ, (1 + ಪದಸೂಚಿ * 259) * 512 + 4)[0] for ಪದಸೂಚಿ in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ಡೇಟಾ[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(ಡೇಟಾ)
        ಯಂತ್ರ = ಅಗೋಚರ_ಯಂತ್ರ(ಸ್ಥಾನ / 'build/kernel.elf', 저장매체=매체)
        try:
            ಯಂತ್ರ.ಆಜ್ಞೆ('cat note.txt', ['generation-one'])
            ಯಂತ್ರ.ಆಜ್ಞೆ('cat stored.txt', ['saved-from-C'])
            ಮಾಪನ['checksum_fallback'] = ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ.decode('utf-8', 'replace')
        finally:
            ಯಂತ್ರ.ಮುಚ್ಚು()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        ಯಂತ್ರ = ಅಗೋಚರ_ಯಂತ್ರ(ಸ್ಥಾನ / 'build/kernel.elf', 저장매체=다른매체)
        try:
            ಯಂತ್ರ.ಆಜ್ಞೆ('sync', ['Sync: -19'])
        finally:
            ಯಂತ್ರ.ಮುಚ್ಚು()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        ಮಾಪನ['foreign_disk_unchanged'] = True
    (ಸ್ಥಾನ / 'build/보존시험.json').write_text(json.dumps(ಮಾಪನ, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE ಸ್ಟೋರ್_ಮೌಲ್ಯ/ISO 재부팅/검사합 ಮರಳಿಪಡೆ_ಸ್ಥಿತಿ/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    ಪೂರೈಸು_ಆದೇಶ()
