#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import enembonakalo_yenyani_umatshini

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', 위치 / 'Izixhobo/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def hlela_ixabiso(umatshini, Isiqulatho_ixabiso):
    Phumeza = len(umatshini.ilog_umqolo)
    umatshini.직렬.sendall(('edit note.txt\n' + Isiqulatho_ixabiso + '\n.save\n').encode())
    return umatshini.기다림('jkoros> ', Phumeza)

def ukwenza_umyalelo():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.yila_ufako_nkcukacha(매체)
        umatshini = enembonakalo_yenyani_umatshini(위치 / 'build/kernel.elf', 저장매체=매체)
        try:
            umatshini.Umyalelo('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            hlela_ixabiso(umatshini, 'generation-one')
            umatshini.Umyalelo('sync', ['Sync: 0'])
            hlela_ixabiso(umatshini, 'generation-two')
            umatshini.Umyalelo('sync', ['Sync: 0'])
            hlela_ixabiso(umatshini, 'unsynced-three')
            결과['save'] = umatshini.ilog_umqolo.decode('utf-8', 'replace')
        finally:
            umatshini.Vala()
        umatshini = enembonakalo_yenyani_umatshini(위치 / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = umatshini.Umyalelo('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            umatshini.Umyalelo('cat stored.txt', ['saved-from-C'])
            결과['restore'] = umatshini.ilog_umqolo.decode('utf-8', 'replace')
        finally:
            umatshini.Vala()
        iingcombolo = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', iingcombolo, (1 + indeksa * 259) * 512 + 4)[0] for indeksa in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        iingcombolo[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(iingcombolo)
        umatshini = enembonakalo_yenyani_umatshini(위치 / 'build/kernel.elf', 저장매체=매체)
        try:
            umatshini.Umyalelo('cat note.txt', ['generation-one'])
            umatshini.Umyalelo('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = umatshini.ilog_umqolo.decode('utf-8', 'replace')
        finally:
            umatshini.Vala()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        umatshini = enembonakalo_yenyani_umatshini(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            umatshini.Umyalelo('sync', ['Sync: -19'])
        finally:
            umatshini.Vala()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_ixabiso/ISO 재부팅/검사합 fumana_kwakhona_imo/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    ukwenza_umyalelo()
