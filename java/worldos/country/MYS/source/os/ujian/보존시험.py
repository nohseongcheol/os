#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from ujian_pengguna_rangkaian import mesin_maya

Kedudukan = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', Kedudukan / 'alat/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def edit_VALUE(mesin, Kandungan_VALUE):
    Jalan = len(mesin.LOG_baris)
    mesin.직렬.sendall(('edit note.txt\n' + Kandungan_VALUE + '\n.save\n').encode())
    return mesin.keadaan_tunggu('jkoros> ', Jalan)

def laksanakan_perintah():
    ukuran = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.cipta_pemasukan(매체)
        mesin = mesin_maya(Kedudukan / 'build/kernel.elf', Storan_medium=매체)
        try:
            mesin.Perintah('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            edit_VALUE(mesin, 'generation-one')
            mesin.Perintah('sync', ['Sync: 0'])
            edit_VALUE(mesin, 'generation-two')
            mesin.Perintah('sync', ['Sync: 0'])
            edit_VALUE(mesin, 'unsynced-three')
            ukuran['save'] = mesin.LOG_baris.decode('utf-8', 'replace')
        finally:
            mesin.Tutup()
        mesin = mesin_maya(Kedudukan / 'build/kernel.iso', 'iso', Storan_medium=매체)
        try:
            출력 = mesin.Perintah('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            mesin.Perintah('cat stored.txt', ['saved-from-C'])
            ukuran['restore'] = mesin.LOG_baris.decode('utf-8', 'replace')
        finally:
            mesin.Tutup()
        data = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', data, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        data[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(data)
        mesin = mesin_maya(Kedudukan / 'build/kernel.elf', Storan_medium=매체)
        try:
            mesin.Perintah('cat note.txt', ['generation-one'])
            mesin.Perintah('cat stored.txt', ['saved-from-C'])
            ukuran['checksum_fallback'] = mesin.LOG_baris.decode('utf-8', 'replace')
        finally:
            mesin.Tutup()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        mesin = mesin_maya(Kedudukan / 'build/kernel.elf', Storan_medium=다른매체)
        try:
            mesin.Perintah('sync', ['Sync: -19'])
        finally:
            mesin.Tutup()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        ukuran['foreign_disk_unchanged'] = True
    (Kedudukan / 'build/보존시험.json').write_text(json.dumps(ukuran, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE stor_VALUE/ISO 재부팅/hasil_tambah_semak pulih_status/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    laksanakan_perintah()
