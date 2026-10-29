#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from test_användare_nätverk import VM

position = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('Media_verktyg', position / 'verktyg/Skapa_minne_Media.py')
Media_verktyg = importlib.util.module_from_spec(명세)
명세.loader.exec_module(Media_verktyg)

def ändring_värde(dator, Innehåll_värde):
    Kör = len(dator.LOG_POST)
    dator.직렬.sendall(('edit note.txt\n' + Innehåll_värde + '\n.save\n').encode())
    return dator.tillståndet_Vänta('jkoros> ', Kör)

def köra_kommando():
    RESULTAT = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        Media_värde = Path(임시) / 'files.img'
        Media_verktyg.Skapa_post(Media_värde)
        dator = VM(position / 'build/kernel.elf', minne_medel=Media_värde)
        try:
            dator.kommando('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            ändring_värde(dator, 'generation-one')
            dator.kommando('sync', ['Sync: 0'])
            ändring_värde(dator, 'generation-two')
            dator.kommando('sync', ['Sync: 0'])
            ändring_värde(dator, 'unsynced-three')
            RESULTAT['save'] = dator.LOG_POST.decode('utf-8', 'replace')
        finally:
            dator.Stäng()
        dator = VM(position / 'build/kernel.iso', 'iso', minne_medel=Media_värde)
        try:
            utmatningsposition = dator.kommando('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in utmatningsposition
            dator.kommando('cat stored.txt', ['saved-from-C'])
            RESULTAT['restore'] = dator.LOG_POST.decode('utf-8', 'replace')
        finally:
            dator.Stäng()
        data = bytearray(Media_värde.read_bytes())
        세대들 = [struct.unpack_from('<I', data, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        data[(1 + 최신 * 259 + 3) * 512] ^= 1
        Media_värde.write_bytes(data)
        dator = VM(position / 'build/kernel.elf', minne_medel=Media_värde)
        try:
            dator.kommando('cat note.txt', ['generation-one'])
            dator.kommando('cat stored.txt', ['saved-from-C'])
            RESULTAT['checksum_fallback'] = dator.LOG_POST.decode('utf-8', 'replace')
        finally:
            dator.Stäng()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        Föregående_objekt = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        dator = VM(position / 'build/kernel.elf', minne_medel=다른매체)
        try:
            dator.kommando('sync', ['Sync: -19'])
        finally:
            dator.Stäng()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == Föregående_objekt
        RESULTAT['foreign_disk_unchanged'] = True
    (position / 'build/보존시험.json').write_text(json.dumps(RESULTAT, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_värde/ISO 재부팅/kontrollsumma återställa_status/다른 Media_värde 비변경', flush=True)

if __name__ == '__main__':
    köra_kommando()
