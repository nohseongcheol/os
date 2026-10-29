#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import kendìnuchè_ngwa_komputa

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('midịà_ngwaọrụ', 위치 / 'Ngwaọrụ/mepụta_Nchekwa_midịà.py')
midịà_ngwaọrụ = importlib.util.module_from_spec(명세)
명세.loader.exec_module(midịà_ngwaọrụ)

def dezìmà_valuu(ngwa_komputa, ndịnà_valuu):
    Bido = len(ngwa_komputa.ndekọ_NDEKỌ)
    ngwa_komputa.직렬.sendall(('edit note.txt\n' + ndịnà_valuu + '\n.save\n').encode())
    return ngwa_komputa.기다림('jkoros> ', Bido)

def mee_nnyemiwu():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        midịà_valuu = Path(임시) / 'files.img'
        midịà_ngwaọrụ.mepụta_ndebà(midịà_valuu)
        ngwa_komputa = kendìnuchè_ngwa_komputa(위치 / 'build/kernel.elf', 저장매체=midịà_valuu)
        try:
            ngwa_komputa.Ntiiwu('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            dezìmà_valuu(ngwa_komputa, 'generation-one')
            ngwa_komputa.Ntiiwu('sync', ['Sync: 0'])
            dezìmà_valuu(ngwa_komputa, 'generation-two')
            ngwa_komputa.Ntiiwu('sync', ['Sync: 0'])
            dezìmà_valuu(ngwa_komputa, 'unsynced-three')
            결과['save'] = ngwa_komputa.ndekọ_NDEKỌ.decode('utf-8', 'replace')
        finally:
            ngwa_komputa.Mechie()
        ngwa_komputa = kendìnuchè_ngwa_komputa(위치 / 'build/kernel.iso', 'iso', 저장매체=midịà_valuu)
        try:
            출력 = ngwa_komputa.Ntiiwu('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            ngwa_komputa.Ntiiwu('cat stored.txt', ['saved-from-C'])
            결과['restore'] = ngwa_komputa.ndekọ_NDEKỌ.decode('utf-8', 'replace')
        finally:
            ngwa_komputa.Mechie()
        datà = bytearray(midịà_valuu.read_bytes())
        세대들 = [struct.unpack_from('<I', datà, (1 + indèks * 259) * 512 + 4)[0] for indèks in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        datà[(1 + 최신 * 259 + 3) * 512] ^= 1
        midịà_valuu.write_bytes(datà)
        ngwa_komputa = kendìnuchè_ngwa_komputa(위치 / 'build/kernel.elf', 저장매체=midịà_valuu)
        try:
            ngwa_komputa.Ntiiwu('cat note.txt', ['generation-one'])
            ngwa_komputa.Ntiiwu('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = ngwa_komputa.ndekọ_NDEKỌ.decode('utf-8', 'replace')
        finally:
            ngwa_komputa.Mechie()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        ngwa_komputa = kendìnuchè_ngwa_komputa(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            ngwa_komputa.Ntiiwu('sync', ['Sync: -19'])
        finally:
            ngwa_komputa.Mechie()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_valuu/ISO 재부팅/검사합 nnweghàchi_ọnọdụ/다른 midịà_valuu 비변경', flush=True)

if __name__ == '__main__':
    mee_nnyemiwu()
