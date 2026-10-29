#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import sethalwa_motšhene

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', 위치 / 'Ditholosi/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def rulaganya_boleng(motšhene, Diteng_boleng):
    Diriša = len(motšhene.pego_rei)
    motšhene.직렬.sendall(('edit note.txt\n' + Diteng_boleng + '\n.save\n').encode())
    return motšhene.기다림('jkoros> ', Diriša)

def phethagatša_taelo():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.만들기(매체)
        motšhene = sethalwa_motšhene(위치 / 'build/kernel.elf', 저장매체=매체)
        try:
            motšhene.Taelo('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            rulaganya_boleng(motšhene, 'generation-one')
            motšhene.Taelo('sync', ['Sync: 0'])
            rulaganya_boleng(motšhene, 'generation-two')
            motšhene.Taelo('sync', ['Sync: 0'])
            rulaganya_boleng(motšhene, 'unsynced-three')
            결과['save'] = motšhene.pego_rei.decode('utf-8', 'replace')
        finally:
            motšhene.Tswalela()
        motšhene = sethalwa_motšhene(위치 / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = motšhene.Taelo('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            motšhene.Taelo('cat stored.txt', ['saved-from-C'])
            결과['restore'] = motšhene.pego_rei.decode('utf-8', 'replace')
        finally:
            motšhene.Tswalela()
        data = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', data, (1 + lokela * 259) * 512 + 4)[0] for lokela in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        data[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(data)
        motšhene = sethalwa_motšhene(위치 / 'build/kernel.elf', 저장매체=매체)
        try:
            motšhene.Taelo('cat note.txt', ['generation-one'])
            motšhene.Taelo('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = motšhene.pego_rei.decode('utf-8', 'replace')
        finally:
            motšhene.Tswalela()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        motšhene = sethalwa_motšhene(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            motšhene.Taelo('sync', ['Sync: -19'])
        finally:
            motšhene.Tswalela()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE lota_boleng/ISO 재부팅/검사합 boela_sekeng_boemo/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    phethagatša_taelo()
