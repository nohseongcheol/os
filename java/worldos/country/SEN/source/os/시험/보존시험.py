#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import luy_feeñ_te_jëmmadi_masin

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('yebuwaay_jumtukaay', 위치 / 'Jumtukaay_yi/sos_Dencukaay_yebuwaay.py')
yebuwaay_jumtukaay = importlib.util.module_from_spec(명세)
명세.loader.exec_module(yebuwaay_jumtukaay)

def soppi_xëyma(masin, Këmb_xëyma):
    daw = len(masin.làq_Dënk)
    masin.직렬.sendall(('edit note.txt\n' + Këmb_xëyma + '\n.save\n').encode())
    return masin.기다림('jkoros> ', daw)

def def_ndigel():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        yebuwaay_xëyma = Path(임시) / 'files.img'
        yebuwaay_jumtukaay.sos_dugal_xabaar(yebuwaay_xëyma)
        masin = luy_feeñ_te_jëmmadi_masin(위치 / 'build/kernel.elf', 저장매체=yebuwaay_xëyma)
        try:
            masin.ndigel('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            soppi_xëyma(masin, 'generation-one')
            masin.ndigel('sync', ['Sync: 0'])
            soppi_xëyma(masin, 'generation-two')
            masin.ndigel('sync', ['Sync: 0'])
            soppi_xëyma(masin, 'unsynced-three')
            결과['save'] = masin.làq_Dënk.decode('utf-8', 'replace')
        finally:
            masin.Tej()
        masin = luy_feeñ_te_jëmmadi_masin(위치 / 'build/kernel.iso', 'iso', 저장매체=yebuwaay_xëyma)
        try:
            출력 = masin.ndigel('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            masin.ndigel('cat stored.txt', ['saved-from-C'])
            결과['restore'] = masin.làq_Dënk.decode('utf-8', 'replace')
        finally:
            masin.Tej()
        mbir = bytearray(yebuwaay_xëyma.read_bytes())
        세대들 = [struct.unpack_from('<I', mbir, (1 + àlluwa_tur * 259) * 512 + 4)[0] for àlluwa_tur in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        mbir[(1 + 최신 * 259 + 3) * 512] ^= 1
        yebuwaay_xëyma.write_bytes(mbir)
        masin = luy_feeñ_te_jëmmadi_masin(위치 / 'build/kernel.elf', 저장매체=yebuwaay_xëyma)
        try:
            masin.ndigel('cat note.txt', ['generation-one'])
            masin.ndigel('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = masin.làq_Dënk.decode('utf-8', 'replace')
        finally:
            masin.Tej()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        masin = luy_feeñ_te_jëmmadi_masin(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            masin.ndigel('sync', ['Sync: -19'])
        finally:
            masin.Tej()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_xëyma/ISO 재부팅/검사합 defaru_nekkin/다른 yebuwaay_xëyma 비변경', flush=True)

if __name__ == '__main__':
    def_ndigel()
