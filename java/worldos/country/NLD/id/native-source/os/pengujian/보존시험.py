#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import mesin_virtual

posisi = Path(__file__).resolve().parents[1]
spes = importlib.util.spec_from_file_location('media_alat', posisi / 'alat/Buat_Storage_media.py')
media_alat = importlib.util.module_from_spec(spes)
spes.loader.exec_module(media_alat)

def Edit_VALUE(mesin, Isi_VALUE):
    jalankan = len(mesin.LOG_baris)
    mesin.직렬.sendall(('edit note.txt\n' + Isi_VALUE + '\n.save\n').encode())
    return mesin.tunggu_Status('jkoros> ', jalankan)

def Jalankan_perintah():
    hasil = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        media_VALUE = Path(임시) / 'files.img'
        media_alat.Buat_entri(media_VALUE)
        mesin = mesin_virtual(posisi / 'build/kernel.elf', 저장매체=media_VALUE)
        try:
            mesin.perintah('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Edit_VALUE(mesin, 'generation-one')
            mesin.perintah('sync', ['Sync: 0'])
            Edit_VALUE(mesin, 'generation-two')
            mesin.perintah('sync', ['Sync: 0'])
            Edit_VALUE(mesin, 'unsynced-three')
            hasil['save'] = mesin.LOG_baris.decode('utf-8', 'replace')
        finally:
            mesin.Tutup()
        mesin = mesin_virtual(posisi / 'build/kernel.iso', 'iso', 저장매체=media_VALUE)
        try:
            keluaranTeks = mesin.perintah('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in keluaranTeks
            mesin.perintah('cat stored.txt', ['saved-from-C'])
            hasil['restore'] = mesin.LOG_baris.decode('utf-8', 'replace')
        finally:
            mesin.Tutup()
        data = bytearray(media_VALUE.read_bytes())
        세대들 = [struct.unpack_from('<I', data, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        data[(1 + 최신 * 259 + 3) * 512] ^= 1
        media_VALUE.write_bytes(data)
        mesin = mesin_virtual(posisi / 'build/kernel.elf', 저장매체=media_VALUE)
        try:
            mesin.perintah('cat note.txt', ['generation-one'])
            mesin.perintah('cat stored.txt', ['saved-from-C'])
            hasil['checksum_fallback'] = mesin.LOG_baris.decode('utf-8', 'replace')
        finally:
            mesin.Tutup()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        mesin = mesin_virtual(posisi / 'build/kernel.elf', 저장매체=다른매체)
        try:
            mesin.perintah('sync', ['Sync: -19'])
        finally:
            mesin.Tutup()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        hasil['foreign_disk_unchanged'] = True
    (posisi / 'build/보존시험.json').write_text(json.dumps(hasil, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/checksum pulihkan_Status/다른 media_VALUE 비변경', flush=True)

if __name__ == '__main__':
    Jalankan_perintah()
