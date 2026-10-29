#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import виртуалӣ_компютер

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('медиа_абзор', 위치 / 'Абзорҳо/эҷод_кардан_Захирагоҳ_медиа.py')
медиа_абзор = importlib.util.module_from_spec(명세)
명세.loader.exec_module(медиа_абзор)

def таҳрир_қимат(компютер, Мӯҳтаво_қимат):
    порча = len(компютер.сабт_кардан_сабт)
    компютер.직렬.sendall(('edit note.txt\n' + Мӯҳтаво_қимат + '\n.save\n').encode())
    return компютер.기다림('jkoros> ', порча)

def иҷро_кардан_фармон():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        медиа_қимат = Path(임시) / 'files.img'
        медиа_абзор.эҷод_кардан_ворида(медиа_қимат)
        компютер = виртуалӣ_компютер(위치 / 'build/kernel.elf', 저장매체=медиа_қимат)
        try:
            компютер.фармон('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            таҳрир_қимат(компютер, 'generation-one')
            компютер.фармон('sync', ['Sync: 0'])
            таҳрир_қимат(компютер, 'generation-two')
            компютер.фармон('sync', ['Sync: 0'])
            таҳрир_қимат(компютер, 'unsynced-three')
            결과['save'] = компютер.сабт_кардан_сабт.decode('utf-8', 'replace')
        finally:
            компютер.Пӯшидан()
        компютер = виртуалӣ_компютер(위치 / 'build/kernel.iso', 'iso', 저장매체=медиа_қимат)
        try:
            출력 = компютер.фармон('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            компютер.фармон('cat stored.txt', ['saved-from-C'])
            결과['restore'] = компютер.сабт_кардан_сабт.decode('utf-8', 'replace')
        finally:
            компютер.Пӯшидан()
        иттилоот = bytearray(медиа_қимат.read_bytes())
        세대들 = [struct.unpack_from('<I', иттилоот, (1 + индекс * 259) * 512 + 4)[0] for индекс in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        иттилоот[(1 + 최신 * 259 + 3) * 512] ^= 1
        медиа_қимат.write_bytes(иттилоот)
        компютер = виртуалӣ_компютер(위치 / 'build/kernel.elf', 저장매체=медиа_қимат)
        try:
            компютер.фармон('cat note.txt', ['generation-one'])
            компютер.фармон('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = компютер.сабт_кардан_сабт.decode('utf-8', 'replace')
        finally:
            компютер.Пӯшидан()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        компютер = виртуалӣ_компютер(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            компютер.фармон('sync', ['Sync: -19'])
        finally:
            компютер.Пӯшидан()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE ҳифз_кардан_қимат/ISO 재부팅/검사합 барқарор_кардан_вазъият/다른 медиа_қимат 비변경', flush=True)

if __name__ == '__main__':
    иҷро_кардан_фармон()
