#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import virtueel_masjien

Posisie = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('media_nutsmiddel', Posisie / 'Nutsmiddels/Skep_Berging_media.py')
media_nutsmiddel = importlib.util.module_from_spec(명세)
명세.loader.exec_module(media_nutsmiddel)

def redigeer_VALUE(masjien, Inhoud_VALUE):
    Loop = len(masjien.LOG_ry)
    masjien.직렬.sendall(('edit note.txt\n' + Inhoud_VALUE + '\n.save\n').encode())
    return masjien.wag_stand('jkoros> ', Loop)

def uitvoer_bevel():
    maatreël = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        media_VALUE = Path(임시) / 'files.img'
        media_nutsmiddel.Skep_inskrywing(media_VALUE)
        masjien = virtueel_masjien(Posisie / 'build/kernel.elf', 저장매체=media_VALUE)
        try:
            masjien.Opdrag('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            redigeer_VALUE(masjien, 'generation-one')
            masjien.Opdrag('sync', ['Sync: 0'])
            redigeer_VALUE(masjien, 'generation-two')
            masjien.Opdrag('sync', ['Sync: 0'])
            redigeer_VALUE(masjien, 'unsynced-three')
            maatreël['save'] = masjien.LOG_ry.decode('utf-8', 'replace')
        finally:
            masjien.Sluit()
        masjien = virtueel_masjien(Posisie / 'build/kernel.iso', 'iso', 저장매체=media_VALUE)
        try:
            Afvoer = masjien.Opdrag('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Afvoer
            masjien.Opdrag('cat stored.txt', ['saved-from-C'])
            maatreël['restore'] = masjien.LOG_ry.decode('utf-8', 'replace')
        finally:
            masjien.Sluit()
        data = bytearray(media_VALUE.read_bytes())
        세대들 = [struct.unpack_from('<I', data, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        data[(1 + 최신 * 259 + 3) * 512] ^= 1
        media_VALUE.write_bytes(data)
        masjien = virtueel_masjien(Posisie / 'build/kernel.elf', 저장매체=media_VALUE)
        try:
            masjien.Opdrag('cat note.txt', ['generation-one'])
            masjien.Opdrag('cat stored.txt', ['saved-from-C'])
            maatreël['checksum_fallback'] = masjien.LOG_ry.decode('utf-8', 'replace')
        finally:
            masjien.Sluit()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        masjien = virtueel_masjien(Posisie / 'build/kernel.elf', 저장매체=다른매체)
        try:
            masjien.Opdrag('sync', ['Sync: -19'])
        finally:
            masjien.Sluit()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        maatreël['foreign_disk_unchanged'] = True
    (Posisie / 'build/보존시험.json').write_text(json.dumps(maatreël, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE bêre_VALUE/ISO 재부팅/검사합 herwin_stand/다른 media_VALUE 비변경', flush=True)

if __name__ == '__main__':
    uitvoer_bevel()
