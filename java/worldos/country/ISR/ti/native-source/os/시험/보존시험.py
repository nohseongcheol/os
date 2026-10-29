#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import መሳሊ_ማሽን

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('መራኸቢ_ብዙሃን_መሳርሒ', 위치 / 'መሳርሒታት/ፍጠር_መኽዘን_መራኸቢ_ብዙሃን.py')
መራኸቢ_ብዙሃን_መሳርሒ = importlib.util.module_from_spec(명세)
명세.loader.exec_module(መራኸቢ_ብዙሃን_መሳርሒ)

def ምዕራይ_ዋጋ(ማሽን, ትሕዝቶ_ዋጋ):
    ኣኺድ = len(ማሽን.ምዝጉብ_ሪጋ)
    ማሽን.직렬.sendall(('edit note.txt\n' + ትሕዝቶ_ዋጋ + '\n.save\n').encode())
    return ማሽን.기다림('jkoros> ', ኣኺድ)

def ተግብር_ትእዛዝ():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        መራኸቢ_ብዙሃን_ዋጋ = Path(임시) / 'files.img'
        መራኸቢ_ብዙሃን_መሳርሒ.ፍጠር_ምእታው(መራኸቢ_ብዙሃን_ዋጋ)
        ማሽን = መሳሊ_ማሽን(위치 / 'build/kernel.elf', 저장매체=መራኸቢ_ብዙሃን_ዋጋ)
        try:
            ማሽን.ትእዛዝ('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            ምዕራይ_ዋጋ(ማሽን, 'generation-one')
            ማሽን.ትእዛዝ('sync', ['Sync: 0'])
            ምዕራይ_ዋጋ(ማሽን, 'generation-two')
            ማሽን.ትእዛዝ('sync', ['Sync: 0'])
            ምዕራይ_ዋጋ(ማሽን, 'unsynced-three')
            결과['save'] = ማሽን.ምዝጉብ_ሪጋ.decode('utf-8', 'replace')
        finally:
            ማሽን.ዕጸው()
        ማሽን = መሳሊ_ማሽን(위치 / 'build/kernel.iso', 'iso', 저장매체=መራኸቢ_ብዙሃን_ዋጋ)
        try:
            출력 = ማሽን.ትእዛዝ('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            ማሽን.ትእዛዝ('cat stored.txt', ['saved-from-C'])
            결과['restore'] = ማሽን.ምዝጉብ_ሪጋ.decode('utf-8', 'replace')
        finally:
            ማሽን.ዕጸው()
        ሓበሬታ = bytearray(መራኸቢ_ብዙሃን_ዋጋ.read_bytes())
        세대들 = [struct.unpack_from('<I', ሓበሬታ, (1 + መሐበሪ * 259) * 512 + 4)[0] for መሐበሪ in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ሓበሬታ[(1 + 최신 * 259 + 3) * 512] ^= 1
        መራኸቢ_ብዙሃን_ዋጋ.write_bytes(ሓበሬታ)
        ማሽን = መሳሊ_ማሽን(위치 / 'build/kernel.elf', 저장매체=መራኸቢ_ብዙሃን_ዋጋ)
        try:
            ማሽን.ትእዛዝ('cat note.txt', ['generation-one'])
            ማሽን.ትእዛዝ('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = ማሽን.ምዝጉብ_ሪጋ.decode('utf-8', 'replace')
        finally:
            ማሽን.ዕጸው()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        ማሽን = መሳሊ_ማሽን(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            ማሽን.ትእዛዝ('sync', ['Sync: -19'])
        finally:
            ማሽን.ዕጸው()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE ከዝን_ዋጋ/ISO 재부팅/검사합 መሊስካ_ርከብ_ደረጃ/다른 መራኸቢ_ብዙሃን_ዋጋ 비변경', flush=True)

if __name__ == '__main__':
    ተግብር_ትእዛዝ()
