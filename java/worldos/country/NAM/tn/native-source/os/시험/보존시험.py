#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import seka_motšhine

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', 위치 / 'Thuluse/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def Tseleganya_Boleng(motšhine, Diteng_Boleng):
    dirisa = len(motšhine.rekota_mola)
    motšhine.직렬.sendall(('edit note.txt\n' + Diteng_Boleng + '\n.save\n').encode())
    return motšhine.기다림('jkoros> ', dirisa)

def diragatsa_Taelo():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.tlhama_tsenyo(매체)
        motšhine = seka_motšhine(위치 / 'build/kernel.elf', 저장매체=매체)
        try:
            motšhine.Taelo('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Tseleganya_Boleng(motšhine, 'generation-one')
            motšhine.Taelo('sync', ['Sync: 0'])
            Tseleganya_Boleng(motšhine, 'generation-two')
            motšhine.Taelo('sync', ['Sync: 0'])
            Tseleganya_Boleng(motšhine, 'unsynced-three')
            결과['save'] = motšhine.rekota_mola.decode('utf-8', 'replace')
        finally:
            motšhine.tswala()
        motšhine = seka_motšhine(위치 / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = motšhine.Taelo('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            motšhine.Taelo('cat stored.txt', ['saved-from-C'])
            결과['restore'] = motšhine.rekota_mola.decode('utf-8', 'replace')
        finally:
            motšhine.tswala()
        tshedimosetso = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', tshedimosetso, (1 + tshupane * 259) * 512 + 4)[0] for tshupane in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        tshedimosetso[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(tshedimosetso)
        motšhine = seka_motšhine(위치 / 'build/kernel.elf', 저장매체=매체)
        try:
            motšhine.Taelo('cat note.txt', ['generation-one'])
            motšhine.Taelo('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = motšhine.rekota_mola.decode('utf-8', 'replace')
        finally:
            motšhine.tswala()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        motšhine = seka_motšhine(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            motšhine.Taelo('sync', ['Sync: -19'])
        finally:
            motšhine.tswala()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_Boleng/ISO 재부팅/검사합 busetsa_morago_kemo/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    diragatsa_Taelo()
