#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import VM

Asukoht = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', Asukoht / 'Tööriistad/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def muudatus_VALUE(arvuti, Sisu_VALUE):
    Käivita_2 = len(arvuti.LOG_kirje)
    arvuti.직렬.sendall(('edit note.txt\n' + Sisu_VALUE + '\n.save\n').encode())
    return arvuti.ooteolek('jkoros> ', Käivita_2)

def Täida_käsk():
    TULEMUS = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.avama_kirje(매체)
        arvuti = VM(Asukoht / 'build/kernel.elf', salvesti_kandja=매체)
        try:
            arvuti.Käsk('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            muudatus_VALUE(arvuti, 'generation-one')
            arvuti.Käsk('sync', ['Sync: 0'])
            muudatus_VALUE(arvuti, 'generation-two')
            arvuti.Käsk('sync', ['Sync: 0'])
            muudatus_VALUE(arvuti, 'unsynced-three')
            TULEMUS['save'] = arvuti.LOG_kirje.decode('utf-8', 'replace')
        finally:
            arvuti.Suletud()
        arvuti = VM(Asukoht / 'build/kernel.iso', 'iso', salvesti_kandja=매체)
        try:
            Väljund = arvuti.Käsk('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Väljund
            arvuti.Käsk('cat stored.txt', ['saved-from-C'])
            TULEMUS['restore'] = arvuti.LOG_kirje.decode('utf-8', 'replace')
        finally:
            arvuti.Suletud()
        andmed = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', andmed, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        andmed[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(andmed)
        arvuti = VM(Asukoht / 'build/kernel.elf', salvesti_kandja=매체)
        try:
            arvuti.Käsk('cat note.txt', ['generation-one'])
            arvuti.Käsk('cat stored.txt', ['saved-from-C'])
            TULEMUS['checksum_fallback'] = arvuti.LOG_kirje.decode('utf-8', 'replace')
        finally:
            arvuti.Suletud()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        arvuti = VM(Asukoht / 'build/kernel.elf', salvesti_kandja=다른매체)
        try:
            arvuti.Käsk('sync', ['Sync: -19'])
        finally:
            arvuti.Suletud()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        TULEMUS['foreign_disk_unchanged'] = True
    (Asukoht / 'build/보존시험.json').write_text(json.dumps(TULEMUS, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE salv_VALUE/ISO 재부팅/kontrollsumma taastama_Olek/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    Täida_käsk()
