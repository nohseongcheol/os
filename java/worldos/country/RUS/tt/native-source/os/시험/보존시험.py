#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import виртуаль_машина

урнаштыру = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('туплагыч_чара', урнаштыру / 'Кораллар/Төзү_Саклагыч_туплагыч.py')
туплагыч_чара = importlib.util.module_from_spec(명세)
명세.loader.exec_module(туплагыч_чара)

def төзәтү_VALUE(машина, Эчтәлек_VALUE):
    эшләтү = len(машина.LOG_юл)
    машина.직렬.sendall(('edit note.txt\n' + Эчтәлек_VALUE + '\n.save\n').encode())
    return машина.기다림('jkoros> ', эшләтү)

def үтәргә_команда():
    үлчәм = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        туплагыч_VALUE = Path(임시) / 'files.img'
        туплагыч_чара.Төзү_кертү(туплагыч_VALUE)
        машина = виртуаль_машина(урнаштыру / 'build/kernel.elf', 저장매체=туплагыч_VALUE)
        try:
            машина.команда('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            төзәтү_VALUE(машина, 'generation-one')
            машина.команда('sync', ['Sync: 0'])
            төзәтү_VALUE(машина, 'generation-two')
            машина.команда('sync', ['Sync: 0'])
            төзәтү_VALUE(машина, 'unsynced-three')
            үлчәм['save'] = машина.LOG_юл.decode('utf-8', 'replace')
        finally:
            машина.Yap()
        машина = виртуаль_машина(урнаштыру / 'build/kernel.iso', 'iso', 저장매체=туплагыч_VALUE)
        try:
            출력 = машина.команда('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            машина.команда('cat stored.txt', ['saved-from-C'])
            үлчәм['restore'] = машина.LOG_юл.decode('utf-8', 'replace')
        finally:
            машина.Yap()
        мәгълүмат = bytearray(туплагыч_VALUE.read_bytes())
        세대들 = [struct.unpack_from('<I', мәгълүмат, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        мәгълүмат[(1 + 최신 * 259 + 3) * 512] ^= 1
        туплагыч_VALUE.write_bytes(мәгълүмат)
        машина = виртуаль_машина(урнаштыру / 'build/kernel.elf', 저장매체=туплагыч_VALUE)
        try:
            машина.команда('cat note.txt', ['generation-one'])
            машина.команда('cat stored.txt', ['saved-from-C'])
            үлчәм['checksum_fallback'] = машина.LOG_юл.decode('utf-8', 'replace')
        finally:
            машина.Yap()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        машина = виртуаль_машина(урнаштыру / 'build/kernel.elf', 저장매체=다른매체)
        try:
            машина.команда('sync', ['Sync: -19'])
        finally:
            машина.Yap()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        үлчәм['foreign_disk_unchanged'] = True
    (урнаштыру / 'build/보존시험.json').write_text(json.dumps(үлчәм, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/검사합 тергезү_халәт/다른 туплагыч_VALUE 비변경', flush=True)

if __name__ == '__main__':
    үтәргә_команда()
