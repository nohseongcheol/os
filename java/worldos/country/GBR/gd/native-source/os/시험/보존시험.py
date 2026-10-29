#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import mas_fhìor_inneal

suidhich = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('meadhanan_inneal', suidhich / 'innealan/Create_stòras_meadhanan.py')
meadhanan_inneal = importlib.util.module_from_spec(명세)
명세.loader.exec_module(meadhanan_inneal)

def deasaich_VALUE(inneal, susbaint_VALUE):
    ruith = len(inneal.LOG_ràgh)
    inneal.직렬.sendall(('edit note.txt\n' + susbaint_VALUE + '\n.save\n').encode())
    return inneal.fuirich_cor('jkoros> ', ruith)

def gnìomhaich_àithne():
    tomhas = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        meadhanan_VALUE = Path(임시) / 'files.img'
        meadhanan_inneal.Create_cur_a_steach(meadhanan_VALUE)
        inneal = mas_fhìor_inneal(suidhich / 'build/kernel.elf', stòras_meadhanach=meadhanan_VALUE)
        try:
            inneal.àithne('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            deasaich_VALUE(inneal, 'generation-one')
            inneal.àithne('sync', ['Sync: 0'])
            deasaich_VALUE(inneal, 'generation-two')
            inneal.àithne('sync', ['Sync: 0'])
            deasaich_VALUE(inneal, 'unsynced-three')
            tomhas['save'] = inneal.LOG_ràgh.decode('utf-8', 'replace')
        finally:
            inneal.dùin()
        inneal = mas_fhìor_inneal(suidhich / 'build/kernel.iso', 'iso', stòras_meadhanach=meadhanan_VALUE)
        try:
            출력 = inneal.àithne('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            inneal.àithne('cat stored.txt', ['saved-from-C'])
            tomhas['restore'] = inneal.LOG_ràgh.decode('utf-8', 'replace')
        finally:
            inneal.dùin()
        dàta = bytearray(meadhanan_VALUE.read_bytes())
        세대들 = [struct.unpack_from('<I', dàta, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        dàta[(1 + 최신 * 259 + 3) * 512] ^= 1
        meadhanan_VALUE.write_bytes(dàta)
        inneal = mas_fhìor_inneal(suidhich / 'build/kernel.elf', stòras_meadhanach=meadhanan_VALUE)
        try:
            inneal.àithne('cat note.txt', ['generation-one'])
            inneal.àithne('cat stored.txt', ['saved-from-C'])
            tomhas['checksum_fallback'] = inneal.LOG_ràgh.decode('utf-8', 'replace')
        finally:
            inneal.dùin()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        inneal = mas_fhìor_inneal(suidhich / 'build/kernel.elf', stòras_meadhanach=다른매체)
        try:
            inneal.àithne('sync', ['Sync: -19'])
        finally:
            inneal.dùin()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        tomhas['foreign_disk_unchanged'] = True
    (suidhich / 'build/보존시험.json').write_text(json.dumps(tomhas, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/검사합 aisig_cor/다른 meadhanan_VALUE 비변경', flush=True)

if __name__ == '__main__':
    gnìomhaich_àithne()
