#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import ምናባዊ_ማሽን

አካባቢ = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', አካባቢ / 'መሳሪያዎች/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def አርትዕ_እሴት(ማሽን, ይዘት_እሴት):
    ማስኬጃ = len(ማሽን.መዝግብ_ረድፍ)
    ማሽን.직렬.sendall(('edit note.txt\n' + ይዘት_እሴት + '\n.save\n').encode())
    return ማሽን.መጠበቅ_ዞን('jkoros> ', ማስኬጃ)

def ፈጽም_ትእዛዝ():
    ልኬት = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.ፍጠር_ምዝግብ(매체)
        ማሽን = ምናባዊ_ማሽን(አካባቢ / 'build/kernel.elf', 저장매체=매체)
        try:
            ማሽን.ትእዛዝ('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            አርትዕ_እሴት(ማሽን, 'generation-one')
            ማሽን.ትእዛዝ('sync', ['Sync: 0'])
            አርትዕ_እሴት(ማሽን, 'generation-two')
            ማሽን.ትእዛዝ('sync', ['Sync: 0'])
            አርትዕ_እሴት(ማሽን, 'unsynced-three')
            ልኬት['save'] = ማሽን.መዝግብ_ረድፍ.decode('utf-8', 'replace')
        finally:
            ማሽን.መዝጊያ()
        ማሽን = ምናባዊ_ማሽን(አካባቢ / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            ውጤት = ማሽን.ትእዛዝ('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in ውጤት
            ማሽን.ትእዛዝ('cat stored.txt', ['saved-from-C'])
            ልኬት['restore'] = ማሽን.መዝግብ_ረድፍ.decode('utf-8', 'replace')
        finally:
            ማሽን.መዝጊያ()
        ውሂብ = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', ውሂብ, (1 + መረጃ_ጠቆመ * 259) * 512 + 4)[0] for መረጃ_ጠቆመ in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ውሂብ[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(ውሂብ)
        ማሽን = ምናባዊ_ማሽን(አካባቢ / 'build/kernel.elf', 저장매체=매체)
        try:
            ማሽን.ትእዛዝ('cat note.txt', ['generation-one'])
            ማሽን.ትእዛዝ('cat stored.txt', ['saved-from-C'])
            ልኬት['checksum_fallback'] = ማሽን.መዝግብ_ረድፍ.decode('utf-8', 'replace')
        finally:
            ማሽን.መዝጊያ()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        ማሽን = ምናባዊ_ማሽን(አካባቢ / 'build/kernel.elf', 저장매체=다른매체)
        try:
            ማሽን.ትእዛዝ('sync', ['Sync: -19'])
        finally:
            ማሽን.መዝጊያ()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        ልኬት['foreign_disk_unchanged'] = True
    (አካባቢ / 'build/보존시험.json').write_text(json.dumps(ልኬት, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE ማከማቻ_እሴት/ISO 재부팅/ድምር_ፍተሻ ወደ_ነበረበት_መልስ_ዞን/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    ፈጽም_ትእዛዝ()
