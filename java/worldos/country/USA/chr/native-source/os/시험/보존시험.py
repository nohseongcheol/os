#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from ᎠᏓᎪᎵᏰᏍᎩ_ᎬᏗᏍᎩ_ᏧᎾᏚᏓᎵ import 가상기계

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('ᎦᎶᏙᏗ_ᎬᏔᏂᏓᏍᏗ', 위치 / '도구/저장매체만들기.py')
ᎦᎶᏙᏗ_ᎬᏔᏂᏓᏍᏗ = importlib.util.module_from_spec(명세)
명세.loader.exec_module(ᎦᎶᏙᏗ_ᎬᏔᏂᏓᏍᏗ)

def ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ):
    ᎠᎢᏎᏍᏗ = len(기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
    기계.직렬.sendall(('edit note.txt\n' + ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ + '\n.save\n').encode())
    return 기계.기다림('jkoros> ', ᎠᎢᏎᏍᏗ)

def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        ᎦᎶᏙᏗ_ᏧᎬᏩᎶᏗᏯ = Path(임시) / 'files.img'
        ᎦᎶᏙᏗ_ᎬᏔᏂᏓᏍᏗ.만들기(ᎦᎶᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
        기계 = 가상기계(위치 / 'build/kernel.elf', 저장매체=ᎦᎶᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
        try:
            기계.ᎤᏁᏤᎸᎩ('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, 'generation-one')
            기계.ᎤᏁᏤᎸᎩ('sync', ['Sync: 0'])
            ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, 'generation-two')
            기계.ᎤᏁᏤᎸᎩ('sync', ['Sync: 0'])
            ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, 'unsynced-three')
            결과['save'] = 기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.decode('utf-8', 'replace')
        finally:
            기계.ᎯᏍᏚᎲᎦ()
        기계 = 가상기계(위치 / 'build/kernel.iso', 'iso', 저장매체=ᎦᎶᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
        try:
            출력 = 기계.ᎤᏁᏤᎸᎩ('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            기계.ᎤᏁᏤᎸᎩ('cat stored.txt', ['saved-from-C'])
            결과['restore'] = 기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.decode('utf-8', 'replace')
        finally:
            기계.ᎯᏍᏚᎲᎦ()
        ᎦᏟᏌᏅᎯ = bytearray(ᎦᎶᏙᏗ_ᏧᎬᏩᎶᏗᏯ.read_bytes())
        세대들 = [struct.unpack_from('<I', ᎦᏟᏌᏅᎯ, (1 + ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ * 259) * 512 + 4)[0] for ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ᎦᏟᏌᏅᎯ[(1 + 최신 * 259 + 3) * 512] ^= 1
        ᎦᎶᏙᏗ_ᏧᎬᏩᎶᏗᏯ.write_bytes(ᎦᏟᏌᏅᎯ)
        기계 = 가상기계(위치 / 'build/kernel.elf', 저장매체=ᎦᎶᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
        try:
            기계.ᎤᏁᏤᎸᎩ('cat note.txt', ['generation-one'])
            기계.ᎤᏁᏤᎸᎩ('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = 기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.decode('utf-8', 'replace')
        finally:
            기계.ᎯᏍᏚᎲᎦ()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        기계 = 가상기계(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            기계.ᎤᏁᏤᎸᎩ('sync', ['Sync: -19'])
        finally:
            기계.ᎯᏍᏚᎲᎦ()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_ᏧᎬᏩᎶᏗᏯ/ISO 재부팅/검사합 ᎠᏩᏛᏗ_ᏄᏍᏗᏓᏅ/다른 ᎦᎶᏙᏗ_ᏧᎬᏩᎶᏗᏯ 비변경', flush=True)

if __name__ == '__main__':
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
