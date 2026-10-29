#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import virtuell_maskin

Posisjon = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', Posisjon / 'Verktøy/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def redigere_VALUE(maskin, Innhald_VALUE):
    Køyr_2 = len(maskin.LOG_rad)
    maskin.직렬.sendall(('edit note.txt\n' + Innhald_VALUE + '\n.save\n').encode())
    return maskin.vent_status('jkoros> ', Køyr_2)

def Utfør_kommando():
    forretningsmål = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.Opprett_oppføring(매체)
        maskin = virtuell_maskin(Posisjon / 'build/kernel.elf', Lagring_medium=매체)
        try:
            maskin.Kommando('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            redigere_VALUE(maskin, 'generation-one')
            maskin.Kommando('sync', ['Sync: 0'])
            redigere_VALUE(maskin, 'generation-two')
            maskin.Kommando('sync', ['Sync: 0'])
            redigere_VALUE(maskin, 'unsynced-three')
            forretningsmål['save'] = maskin.LOG_rad.decode('utf-8', 'replace')
        finally:
            maskin.Lukk()
        maskin = virtuell_maskin(Posisjon / 'build/kernel.iso', 'iso', Lagring_medium=매체)
        try:
            Utdata = maskin.Kommando('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Utdata
            maskin.Kommando('cat stored.txt', ['saved-from-C'])
            forretningsmål['restore'] = maskin.LOG_rad.decode('utf-8', 'replace')
        finally:
            maskin.Lukk()
        data = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', data, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        data[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(data)
        maskin = virtuell_maskin(Posisjon / 'build/kernel.elf', Lagring_medium=매체)
        try:
            maskin.Kommando('cat note.txt', ['generation-one'])
            maskin.Kommando('cat stored.txt', ['saved-from-C'])
            forretningsmål['checksum_fallback'] = maskin.LOG_rad.decode('utf-8', 'replace')
        finally:
            maskin.Lukk()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        maskin = virtuell_maskin(Posisjon / 'build/kernel.elf', Lagring_medium=다른매체)
        try:
            maskin.Kommando('sync', ['Sync: -19'])
        finally:
            maskin.Lukk()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        forretningsmål['foreign_disk_unchanged'] = True
    (Posisjon / 'build/보존시험.json').write_text(json.dumps(forretningsmål, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/kontrollsum gjenopprette_status/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    Utfør_kommando()
