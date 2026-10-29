#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import makina_birtual

Posizioa = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', Posizioa / 'Tresnak/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def edizio_balio(gailu, eduki_balio):
    Exekutatu_2 = len(gailu.LOG_marka)
    gailu.직렬.sendall(('edit note.txt\n' + eduki_balio + '\n.save\n').encode())
    return gailu.itxaron_Egoera('jkoros> ', Exekutatu_2)

def exekutatu_komando():
    EMAITZA = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.sortu_sarrera(매체)
        gailu = makina_birtual(Posizioa / 'build/kernel.elf', 저장매체=매체)
        try:
            gailu.Komandoa('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            edizio_balio(gailu, 'generation-one')
            gailu.Komandoa('sync', ['Sync: 0'])
            edizio_balio(gailu, 'generation-two')
            gailu.Komandoa('sync', ['Sync: 0'])
            edizio_balio(gailu, 'unsynced-three')
            EMAITZA['save'] = gailu.LOG_marka.decode('utf-8', 'replace')
        finally:
            gailu.Itxi()
        gailu = makina_birtual(Posizioa / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            Irteera = gailu.Komandoa('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Irteera
            gailu.Komandoa('cat stored.txt', ['saved-from-C'])
            EMAITZA['restore'] = gailu.LOG_marka.decode('utf-8', 'replace')
        finally:
            gailu.Itxi()
        datuak = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', datuak, (1 + INDIZE * 259) * 512 + 4)[0] for INDIZE in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        datuak[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(datuak)
        gailu = makina_birtual(Posizioa / 'build/kernel.elf', 저장매체=매체)
        try:
            gailu.Komandoa('cat note.txt', ['generation-one'])
            gailu.Komandoa('cat stored.txt', ['saved-from-C'])
            EMAITZA['checksum_fallback'] = gailu.LOG_marka.decode('utf-8', 'replace')
        finally:
            gailu.Itxi()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        gailu = makina_birtual(Posizioa / 'build/kernel.elf', 저장매체=다른매체)
        try:
            gailu.Komandoa('sync', ['Sync: -19'])
        finally:
            gailu.Itxi()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        EMAITZA['foreign_disk_unchanged'] = True
    (Posizioa / 'build/보존시험.json').write_text(json.dumps(EMAITZA, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_balio/ISO 재부팅/kontroleko_batura oneratu_Egoera/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    exekutatu_komando()
