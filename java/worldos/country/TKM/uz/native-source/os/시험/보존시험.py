#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import 가상기계

Holati = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', Holati / 'Vositalar/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def tahrirlamoq_VALUE(기계, tarkib_VALUE):
    Bajarish = len(기계.LOG_satr)
    기계.직렬.sendall(('edit note.txt\n' + tarkib_VALUE + '\n.save\n').encode())
    return 기계.bir_daqiqa_holat('jkoros> ', Bajarish)

def bajarmoq_buyruq():
    o_lchov = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.Yaratish_kiritish(매체)
        기계 = 가상기계(Holati / 'build/kernel.elf', 저장매체=매체)
        try:
            기계.Buyruq('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            tahrirlamoq_VALUE(기계, 'generation-one')
            기계.Buyruq('sync', ['Sync: 0'])
            tahrirlamoq_VALUE(기계, 'generation-two')
            기계.Buyruq('sync', ['Sync: 0'])
            tahrirlamoq_VALUE(기계, 'unsynced-three')
            o_lchov['save'] = 기계.LOG_satr.decode('utf-8', 'replace')
        finally:
            기계.Yopish()
        기계 = 가상기계(Holati / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = 기계.Buyruq('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            기계.Buyruq('cat stored.txt', ['saved-from-C'])
            o_lchov['restore'] = 기계.LOG_satr.decode('utf-8', 'replace')
        finally:
            기계.Yopish()
        ma_lumotlar = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', ma_lumotlar, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ma_lumotlar[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(ma_lumotlar)
        기계 = 가상기계(Holati / 'build/kernel.elf', 저장매체=매체)
        try:
            기계.Buyruq('cat note.txt', ['generation-one'])
            기계.Buyruq('cat stored.txt', ['saved-from-C'])
            o_lchov['checksum_fallback'] = 기계.LOG_satr.decode('utf-8', 'replace')
        finally:
            기계.Yopish()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        기계 = 가상기계(Holati / 'build/kernel.elf', 저장매체=다른매체)
        try:
            기계.Buyruq('sync', ['Sync: -19'])
        finally:
            기계.Yopish()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        o_lchov['foreign_disk_unchanged'] = True
    (Holati / 'build/보존시험.json').write_text(json.dumps(o_lchov, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/검사합 tiklamoq_holat/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    bajarmoq_buyruq()
