#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import virtual_makinë

Pozicioni = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', Pozicioni / 'Mjete/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def redaktim_VALUE(makinë, Përmbajtje_VALUE):
    Ekzekuto = len(makinë.LOG_RECORD)
    makinë.직렬.sendall(('edit note.txt\n' + Përmbajtje_VALUE + '\n.save\n').encode())
    return makinë.Prit_status('jkoros> ', Ekzekuto)

def zbatoj_komandë():
    llogaritje = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.Krijo_futje(매체)
        makinë = virtual_makinë(Pozicioni / 'build/kernel.elf', 저장매체=매체)
        try:
            makinë.Komanda('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            redaktim_VALUE(makinë, 'generation-one')
            makinë.Komanda('sync', ['Sync: 0'])
            redaktim_VALUE(makinë, 'generation-two')
            makinë.Komanda('sync', ['Sync: 0'])
            redaktim_VALUE(makinë, 'unsynced-three')
            llogaritje['save'] = makinë.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            makinë.Mbyll()
        makinë = virtual_makinë(Pozicioni / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = makinë.Komanda('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            makinë.Komanda('cat stored.txt', ['saved-from-C'])
            llogaritje['restore'] = makinë.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            makinë.Mbyll()
        të_dhëna = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', të_dhëna, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        të_dhëna[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(të_dhëna)
        makinë = virtual_makinë(Pozicioni / 'build/kernel.elf', 저장매체=매체)
        try:
            makinë.Komanda('cat note.txt', ['generation-one'])
            makinë.Komanda('cat stored.txt', ['saved-from-C'])
            llogaritje['checksum_fallback'] = makinë.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            makinë.Mbyll()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        makinë = virtual_makinë(Pozicioni / 'build/kernel.elf', 저장매체=다른매체)
        try:
            makinë.Komanda('sync', ['Sync: -19'])
        finally:
            makinë.Mbyll()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        llogaritje['foreign_disk_unchanged'] = True
    (Pozicioni / 'build/보존시험.json').write_text(json.dumps(llogaritje, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/kontrolli_i_shumës rikuperoj_status/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    zbatoj_komandë()
