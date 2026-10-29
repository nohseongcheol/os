#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import виртуелно_рачунар

Положај = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', Положај / 'Алатке/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def Уреди_вриједност(рачунар, Садржај_вриједност):
    Покрени = len(рачунар.евиденција_ред)
    рачунар.직렬.sendall(('edit note.txt\n' + Садржај_вриједност + '\n.save\n').encode())
    return рачунар.чекај_стање('jkoros> ', Покрени)

def Изврши_команда():
    ИСХОД = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.Направи_унос(매체)
        рачунар = виртуелно_рачунар(Положај / 'build/kernel.elf', 저장매체=매체)
        try:
            рачунар.Наредба('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Уреди_вриједност(рачунар, 'generation-one')
            рачунар.Наредба('sync', ['Sync: 0'])
            Уреди_вриједност(рачунар, 'generation-two')
            рачунар.Наредба('sync', ['Sync: 0'])
            Уреди_вриједност(рачунар, 'unsynced-three')
            ИСХОД['save'] = рачунар.евиденција_ред.decode('utf-8', 'replace')
        finally:
            рачунар.Затворен()
        рачунар = виртуелно_рачунар(Положај / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            Излаз = рачунар.Наредба('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Излаз
            рачунар.Наредба('cat stored.txt', ['saved-from-C'])
            ИСХОД['restore'] = рачунар.евиденција_ред.decode('utf-8', 'replace')
        finally:
            рачунар.Затворен()
        подаци = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', подаци, (1 + индекс * 259) * 512 + 4)[0] for индекс in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        подаци[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(подаци)
        рачунар = виртуелно_рачунар(Положај / 'build/kernel.elf', 저장매체=매체)
        try:
            рачунар.Наредба('cat note.txt', ['generation-one'])
            рачунар.Наредба('cat stored.txt', ['saved-from-C'])
            ИСХОД['checksum_fallback'] = рачунар.евиденција_ред.decode('utf-8', 'replace')
        finally:
            рачунар.Затворен()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        рачунар = виртуелно_рачунар(Положај / 'build/kernel.elf', 저장매체=다른매체)
        try:
            рачунар.Наредба('sync', ['Sync: -19'])
        finally:
            рачунар.Затворен()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        ИСХОД['foreign_disk_unchanged'] = True
    (Положај / 'build/보존시험.json').write_text(json.dumps(ИСХОД, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE похранити_вриједност/ISO 재부팅/контролни_збир опоравити_стање/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    Изврши_команда()
