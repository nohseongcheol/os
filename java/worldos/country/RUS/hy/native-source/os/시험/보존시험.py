#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import վիրտուալ_մեքենա

Դիրք = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', Դիրք / 'Գործիքներ/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def խմբագրել_արժեք(մեքենա, Բովանդակություն_արժեք):
    Գործարկել = len(մեքենա.մատյան_տող)
    մեքենա.직렬.sendall(('edit note.txt\n' + Բովանդակություն_արժեք + '\n.save\n').encode())
    return մեքենա.기다림('jkoros> ', Գործարկել)

def կատարել_հրաման():
    չափ = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.Կերտի_ր_մուտքագրում(매체)
        մեքենա = վիրտուալ_մեքենա(Դիրք / 'build/kernel.elf', 저장매체=매체)
        try:
            մեքենա.Հրահանգ('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            խմբագրել_արժեք(մեքենա, 'generation-one')
            մեքենա.Հրահանգ('sync', ['Sync: 0'])
            խմբագրել_արժեք(մեքենա, 'generation-two')
            մեքենա.Հրահանգ('sync', ['Sync: 0'])
            խմբագրել_արժեք(մեքենա, 'unsynced-three')
            չափ['save'] = մեքենա.մատյան_տող.decode('utf-8', 'replace')
        finally:
            մեքենա.Փակ()
        մեքենա = վիրտուալ_մեքենա(Դիրք / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            Ելք = մեքենա.Հրահանգ('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Ելք
            մեքենա.Հրահանգ('cat stored.txt', ['saved-from-C'])
            չափ['restore'] = մեքենա.մատյան_տող.decode('utf-8', 'replace')
        finally:
            մեքենա.Փակ()
        տվյալ = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', տվյալ, (1 + դասիչ * 259) * 512 + 4)[0] for դասիչ in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        տվյալ[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(տվյալ)
        մեքենա = վիրտուալ_մեքենա(Դիրք / 'build/kernel.elf', 저장매체=매체)
        try:
            մեքենա.Հրահանգ('cat note.txt', ['generation-one'])
            մեքենա.Հրահանգ('cat stored.txt', ['saved-from-C'])
            չափ['checksum_fallback'] = մեքենա.մատյան_տող.decode('utf-8', 'replace')
        finally:
            մեքենա.Փակ()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        մեքենա = վիրտուալ_մեքենա(Դիրք / 'build/kernel.elf', 저장매체=다른매체)
        try:
            մեքենա.Հրահանգ('sync', ['Sync: -19'])
        finally:
            մեքենա.Փակ()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        չափ['foreign_disk_unchanged'] = True
    (Դիրք / 'build/보존시험.json').write_text(json.dumps(չափ, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE պահեստավորել_արժեք/ISO 재부팅/검사합 վերականգնել_վիճակ/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    կատարել_հրաման()
