#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import pepe_mashine

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', 위치 / 'Zana/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def hariri_thamani(mashine, maudhui_thamani):
    endesha = len(mashine.batli_REKODI)
    mashine.직렬.sendall(('edit note.txt\n' + maudhui_thamani + '\n.save\n').encode())
    return mashine.subiri_hali('jkoros> ', endesha)

def tekeleza_amri():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.unda_ingizo(매체)
        mashine = pepe_mashine(위치 / 'build/kernel.elf', 저장매체=매체)
        try:
            mashine.amri('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            hariri_thamani(mashine, 'generation-one')
            mashine.amri('sync', ['Sync: 0'])
            hariri_thamani(mashine, 'generation-two')
            mashine.amri('sync', ['Sync: 0'])
            hariri_thamani(mashine, 'unsynced-three')
            결과['save'] = mashine.batli_REKODI.decode('utf-8', 'replace')
        finally:
            mashine.funga()
        mashine = pepe_mashine(위치 / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = mashine.amri('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            mashine.amri('cat stored.txt', ['saved-from-C'])
            결과['restore'] = mashine.batli_REKODI.decode('utf-8', 'replace')
        finally:
            mashine.funga()
        data = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', data, (1 + kielezo * 259) * 512 + 4)[0] for kielezo in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        data[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(data)
        mashine = pepe_mashine(위치 / 'build/kernel.elf', 저장매체=매체)
        try:
            mashine.amri('cat note.txt', ['generation-one'])
            mashine.amri('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = mashine.batli_REKODI.decode('utf-8', 'replace')
        finally:
            mashine.funga()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        mashine = pepe_mashine(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            mashine.amri('sync', ['Sync: -19'])
        finally:
            mashine.funga()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_thamani/ISO 재부팅/jumla rejesha_hali/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    tekeleza_amri()
