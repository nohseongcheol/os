#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from test_bruger_netværk import VM

Placering = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('Medie_værktøj', Placering / 'Værktøjer/åbne_Lager_Medie.py')
Medie_værktøj = importlib.util.module_from_spec(명세)
명세.loader.exec_module(Medie_værktøj)

def Rediger_VÆRDI(maskine, Indhold_VÆRDI):
    Kør_2 = len(maskine.LOG_post)
    maskine.직렬.sendall(('edit note.txt\n' + Indhold_VÆRDI + '\n.save\n').encode())
    return maskine.ventetilstand('jkoros> ', Kør_2)

def Udfør_kommando():
    KR = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        Medie_VÆRDI = Path(임시) / 'files.img'
        Medie_værktøj.åbne_post_81b8d99b(Medie_VÆRDI)
        maskine = VM(Placering / 'build/kernel.elf', Lager_medie=Medie_VÆRDI)
        try:
            maskine.Kommando('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Rediger_VÆRDI(maskine, 'generation-one')
            maskine.Kommando('sync', ['Sync: 0'])
            Rediger_VÆRDI(maskine, 'generation-two')
            maskine.Kommando('sync', ['Sync: 0'])
            Rediger_VÆRDI(maskine, 'unsynced-three')
            KR['save'] = maskine.LOG_post.decode('utf-8', 'replace')
        finally:
            maskine.Luk()
        maskine = VM(Placering / 'build/kernel.iso', 'iso', Lager_medie=Medie_VÆRDI)
        try:
            Udgang = maskine.Kommando('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Udgang
            maskine.Kommando('cat stored.txt', ['saved-from-C'])
            KR['restore'] = maskine.LOG_post.decode('utf-8', 'replace')
        finally:
            maskine.Luk()
        data = bytearray(Medie_VÆRDI.read_bytes())
        세대들 = [struct.unpack_from('<I', data, (1 + INDEKS * 259) * 512 + 4)[0] for INDEKS in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        data[(1 + 최신 * 259 + 3) * 512] ^= 1
        Medie_VÆRDI.write_bytes(data)
        maskine = VM(Placering / 'build/kernel.elf', Lager_medie=Medie_VÆRDI)
        try:
            maskine.Kommando('cat note.txt', ['generation-one'])
            maskine.Kommando('cat stored.txt', ['saved-from-C'])
            KR['checksum_fallback'] = maskine.LOG_post.decode('utf-8', 'replace')
        finally:
            maskine.Luk()
        Andet_Medie = Path(임시) / 'foreign.img'
        Andet_Medie.write_bytes(bytes([0x5a]) * (2048 * 512))
        Forrige_vare = hashlib.sha256(Andet_Medie.read_bytes()).hexdigest()
        maskine = VM(Placering / 'build/kernel.elf', Lager_medie=Andet_Medie)
        try:
            maskine.Kommando('sync', ['Sync: -19'])
        finally:
            maskine.Luk()
        assert hashlib.sha256(Andet_Medie.read_bytes()).hexdigest() == Forrige_vare
        KR['foreign_disk_unchanged'] = True
    (Placering / 'build/보존시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VÆRDI/ISO 재부팅/kontrolsum genoprette_status/다른 Medie_VÆRDI 비변경', flush=True)

if __name__ == '__main__':
    Udfør_kommando()
