#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import rhith_peiriant

safle = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', safle / 'Offer/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def Golygu_VALUE(peiriant, Cynnwys_VALUE):
    Gweithredu_2 = len(peiriant.LOG_rhes)
    peiriant.직렬.sendall(('edit note.txt\n' + Cynnwys_VALUE + '\n.save\n').encode())
    return peiriant.aros_cyflwr('jkoros> ', Gweithredu_2)

def Gweithredu_gorchymyn():
    mesur = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.Creu_cofnod(매체)
        peiriant = rhith_peiriant(safle / 'build/kernel.elf', Storio_canolig=매체)
        try:
            peiriant.Gorchymyn('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Golygu_VALUE(peiriant, 'generation-one')
            peiriant.Gorchymyn('sync', ['Sync: 0'])
            Golygu_VALUE(peiriant, 'generation-two')
            peiriant.Gorchymyn('sync', ['Sync: 0'])
            Golygu_VALUE(peiriant, 'unsynced-three')
            mesur['save'] = peiriant.LOG_rhes.decode('utf-8', 'replace')
        finally:
            peiriant.Cau()
        peiriant = rhith_peiriant(safle / 'build/kernel.iso', 'iso', Storio_canolig=매체)
        try:
            Allbwn = peiriant.Gorchymyn('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Allbwn
            peiriant.Gorchymyn('cat stored.txt', ['saved-from-C'])
            mesur['restore'] = peiriant.LOG_rhes.decode('utf-8', 'replace')
        finally:
            peiriant.Cau()
        data = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', data, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        data[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(data)
        peiriant = rhith_peiriant(safle / 'build/kernel.elf', Storio_canolig=매체)
        try:
            peiriant.Gorchymyn('cat note.txt', ['generation-one'])
            peiriant.Gorchymyn('cat stored.txt', ['saved-from-C'])
            mesur['checksum_fallback'] = peiriant.LOG_rhes.decode('utf-8', 'replace')
        finally:
            peiriant.Cau()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        peiriant = rhith_peiriant(safle / 'build/kernel.elf', Storio_canolig=다른매체)
        try:
            peiriant.Gorchymyn('sync', ['Sync: -19'])
        finally:
            peiriant.Cau()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        mesur['foreign_disk_unchanged'] = True
    (safle / 'build/보존시험.json').write_text(json.dumps(mesur, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/prawfswm adfer_cyflwr/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    Gweithredu_gorchymyn()
