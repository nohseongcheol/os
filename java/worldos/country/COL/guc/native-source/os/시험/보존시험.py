#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import 가상기계

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('anaajaaleeirua_a_yataaya', 위치 / '도구/저장매체만들기.py')
anaajaaleeirua_a_yataaya = importlib.util.module_from_spec(명세)
명세.loader.exec_module(anaajaaleeirua_a_yataaya)

def anaataa_ajutuu(기계, alu_ujatüü_ajutuu):
    시작 = len(기계.aa_innachikimaajatü_aparatsee)
    기계.직렬.sendall(('edit note.txt\n' + alu_ujatüü_ajutuu + '\n.save\n').encode())
    return 기계.기다림('jkoros> ', 시작)

def 실행():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        anaajaaleeirua_ajutuu = Path(임시) / 'files.img'
        anaajaaleeirua_a_yataaya.만들기(anaajaaleeirua_ajutuu)
        기계 = 가상기계(위치 / 'build/kernel.elf', 저장매체=anaajaaleeirua_ajutuu)
        try:
            기계.aluwataaya('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            anaataa_ajutuu(기계, 'generation-one')
            기계.aluwataaya('sync', ['Sync: 0'])
            anaataa_ajutuu(기계, 'generation-two')
            기계.aluwataaya('sync', ['Sync: 0'])
            anaataa_ajutuu(기계, 'unsynced-three')
            결과['save'] = 기계.aa_innachikimaajatü_aparatsee.decode('utf-8', 'replace')
        finally:
            기계.asürülaa()
        기계 = 가상기계(위치 / 'build/kernel.iso', 'iso', 저장매체=anaajaaleeirua_ajutuu)
        try:
            출력 = 기계.aluwataaya('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            기계.aluwataaya('cat stored.txt', ['saved-from-C'])
            결과['restore'] = 기계.aa_innachikimaajatü_aparatsee.decode('utf-8', 'replace')
        finally:
            기계.asürülaa()
        atijaaya = bytearray(anaajaaleeirua_ajutuu.read_bytes())
        세대들 = [struct.unpack_from('<I', atijaaya, (1 + ee_iyatialujuna * 259) * 512 + 4)[0] for ee_iyatialujuna in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        atijaaya[(1 + 최신 * 259 + 3) * 512] ^= 1
        anaajaaleeirua_ajutuu.write_bytes(atijaaya)
        기계 = 가상기계(위치 / 'build/kernel.elf', 저장매체=anaajaaleeirua_ajutuu)
        try:
            기계.aluwataaya('cat note.txt', ['generation-one'])
            기계.aluwataaya('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = 기계.aa_innachikimaajatü_aparatsee.decode('utf-8', 'replace')
        finally:
            기계.asürülaa()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        기계 = 가상기계(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            기계.aluwataaya('sync', ['Sync: -19'])
        finally:
            기계.asürülaa()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE 저장/ISO 재부팅/검사합 복구/다른 anaajaaleeirua_ajutuu 비변경', flush=True)

if __name__ == '__main__':
    실행()
