#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import virtual_machine

posisyon = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', posisyon / 'Mga_Tool/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def edit_VALUE(machine, Nilalaman_VALUE):
    run = len(machine.LOG_hanay)
    machine.직렬.sendall(('edit note.txt\n' + Nilalaman_VALUE + '\n.save\n').encode())
    return machine.maghintay_katayuan('jkoros> ', run)

def Mag_execute_utos():
    sukat = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.Create_pagpasok(매체)
        machine = virtual_machine(posisyon / 'build/kernel.elf', 저장매체=매체)
        try:
            machine.utos('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            edit_VALUE(machine, 'generation-one')
            machine.utos('sync', ['Sync: 0'])
            edit_VALUE(machine, 'generation-two')
            machine.utos('sync', ['Sync: 0'])
            edit_VALUE(machine, 'unsynced-three')
            sukat['save'] = machine.LOG_hanay.decode('utf-8', 'replace')
        finally:
            machine.isara()
        machine = virtual_machine(posisyon / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = machine.utos('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            machine.utos('cat stored.txt', ['saved-from-C'])
            sukat['restore'] = machine.LOG_hanay.decode('utf-8', 'replace')
        finally:
            machine.isara()
        data = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', data, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        data[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(data)
        machine = virtual_machine(posisyon / 'build/kernel.elf', 저장매체=매체)
        try:
            machine.utos('cat note.txt', ['generation-one'])
            machine.utos('cat stored.txt', ['saved-from-C'])
            sukat['checksum_fallback'] = machine.LOG_hanay.decode('utf-8', 'replace')
        finally:
            machine.isara()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        machine = virtual_machine(posisyon / 'build/kernel.elf', 저장매체=다른매체)
        try:
            machine.utos('sync', ['Sync: -19'])
        finally:
            machine.isara()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        sukat['foreign_disk_unchanged'] = True
    (posisyon / 'build/보존시험.json').write_text(json.dumps(sukat, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/checksum bawiin_katayuan/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    Mag_execute_utos()
