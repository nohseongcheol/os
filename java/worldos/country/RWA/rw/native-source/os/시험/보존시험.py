#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import kidafatika_imashini

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', 위치 / 'Ibikoresho/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def guhindura_agaciro(imashini, Ibirimo_agaciro):
    ihuriro = len(imashini.kubika_umurongo)
    imashini.직렬.sendall(('edit note.txt\n' + Ibirimo_agaciro + '\n.save\n').encode())
    return imashini.기다림('jkoros> ', ihuriro)

def gukora_ibwiriza():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.kurema_icyinjizwa(매체)
        imashini = kidafatika_imashini(위치 / 'build/kernel.elf', 저장매체=매체)
        try:
            imashini.Icyo_wifuza('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            guhindura_agaciro(imashini, 'generation-one')
            imashini.Icyo_wifuza('sync', ['Sync: 0'])
            guhindura_agaciro(imashini, 'generation-two')
            imashini.Icyo_wifuza('sync', ['Sync: 0'])
            guhindura_agaciro(imashini, 'unsynced-three')
            결과['save'] = imashini.kubika_umurongo.decode('utf-8', 'replace')
        finally:
            imashini.Gufunga()
        imashini = kidafatika_imashini(위치 / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = imashini.Icyo_wifuza('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            imashini.Icyo_wifuza('cat stored.txt', ['saved-from-C'])
            결과['restore'] = imashini.kubika_umurongo.decode('utf-8', 'replace')
        finally:
            imashini.Gufunga()
        amakurushingiro = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', amakurushingiro, (1 + umugerekashakiro * 259) * 512 + 4)[0] for umugerekashakiro in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        amakurushingiro[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(amakurushingiro)
        imashini = kidafatika_imashini(위치 / 'build/kernel.elf', 저장매체=매체)
        try:
            imashini.Icyo_wifuza('cat note.txt', ['generation-one'])
            imashini.Icyo_wifuza('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = imashini.kubika_umurongo.decode('utf-8', 'replace')
        finally:
            imashini.Gufunga()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        imashini = kidafatika_imashini(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            imashini.Icyo_wifuza('sync', ['Sync: -19'])
        finally:
            imashini.Gufunga()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_agaciro/ISO 재부팅/검사합 kugarura_imimerere/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    gukora_ibwiriza()
