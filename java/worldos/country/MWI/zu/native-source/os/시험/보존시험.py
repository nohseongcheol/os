#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import utalagu_umshini

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('imidiya_ithuluzi', 위치 / 'Amathuluzi/yakha_Indawo_yokugcina_imidiya.py')
imidiya_ithuluzi = importlib.util.module_from_spec(명세)
명세.loader.exec_module(imidiya_ithuluzi)

def hlela_inani(umshini, Okuqukethwe_inani):
    Sebenzisa = len(umshini.loga_umugqa)
    umshini.직렬.sendall(('edit note.txt\n' + Okuqukethwe_inani + '\n.save\n').encode())
    return umshini.기다림('jkoros> ', Sebenzisa)

def yenza_umyalo():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        imidiya_inani = Path(임시) / 'files.img'
        imidiya_ithuluzi.yakha_okufakwayo(imidiya_inani)
        umshini = utalagu_umshini(위치 / 'build/kernel.elf', 저장매체=imidiya_inani)
        try:
            umshini.Umlayelo('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            hlela_inani(umshini, 'generation-one')
            umshini.Umlayelo('sync', ['Sync: 0'])
            hlela_inani(umshini, 'generation-two')
            umshini.Umlayelo('sync', ['Sync: 0'])
            hlela_inani(umshini, 'unsynced-three')
            결과['save'] = umshini.loga_umugqa.decode('utf-8', 'replace')
        finally:
            umshini.Vala()
        umshini = utalagu_umshini(위치 / 'build/kernel.iso', 'iso', 저장매체=imidiya_inani)
        try:
            출력 = umshini.Umlayelo('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            umshini.Umlayelo('cat stored.txt', ['saved-from-C'])
            결과['restore'] = umshini.loga_umugqa.decode('utf-8', 'replace')
        finally:
            umshini.Vala()
        imininingwane = bytearray(imidiya_inani.read_bytes())
        세대들 = [struct.unpack_from('<I', imininingwane, (1 + thola_inkomba * 259) * 512 + 4)[0] for thola_inkomba in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        imininingwane[(1 + 최신 * 259 + 3) * 512] ^= 1
        imidiya_inani.write_bytes(imininingwane)
        umshini = utalagu_umshini(위치 / 'build/kernel.elf', 저장매체=imidiya_inani)
        try:
            umshini.Umlayelo('cat note.txt', ['generation-one'])
            umshini.Umlayelo('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = umshini.loga_umugqa.decode('utf-8', 'replace')
        finally:
            umshini.Vala()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        umshini = utalagu_umshini(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            umshini.Umlayelo('sync', ['Sync: -19'])
        finally:
            umshini.Vala()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_inani/ISO 재부팅/검사합 buyisa_isimo/다른 imidiya_inani 비변경', flush=True)

if __name__ == '__main__':
    yenza_umyalo()
