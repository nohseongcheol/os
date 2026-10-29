#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from test_bruker_nettverk import VM

Posisjon = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('media_verktøy', Posisjon / 'Verktøy/åpne_lager_media.py')
media_verktøy = importlib.util.module_from_spec(명세)
명세.loader.exec_module(media_verktøy)

def Rediger_VERDI(maskin, Innhold_VERDI):
    Kjør_2 = len(maskin.LOG_POST)
    maskin.직렬.sendall(('edit note.txt\n' + Innhold_VERDI + '\n.save\n').encode())
    return maskin.ventende_tilstand('jkoros> ', Kjør_2)

def Utfør_kommando():
    KR = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        media_VERDI = Path(임시) / 'files.img'
        media_verktøy.åpne_oppføring(media_VERDI)
        maskin = VM(Posisjon / 'build/kernel.elf', lager_medium=media_VERDI)
        try:
            maskin.Kommando('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Rediger_VERDI(maskin, 'generation-one')
            maskin.Kommando('sync', ['Sync: 0'])
            Rediger_VERDI(maskin, 'generation-two')
            maskin.Kommando('sync', ['Sync: 0'])
            Rediger_VERDI(maskin, 'unsynced-three')
            KR['save'] = maskin.LOG_POST.decode('utf-8', 'replace')
        finally:
            maskin.Lukk()
        maskin = VM(Posisjon / 'build/kernel.iso', 'iso', lager_medium=media_VERDI)
        try:
            Utgang = maskin.Kommando('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Utgang
            maskin.Kommando('cat stored.txt', ['saved-from-C'])
            KR['restore'] = maskin.LOG_POST.decode('utf-8', 'replace')
        finally:
            maskin.Lukk()
        data = bytearray(media_VERDI.read_bytes())
        세대들 = [struct.unpack_from('<I', data, (1 + INDEKS * 259) * 512 + 4)[0] for INDEKS in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        data[(1 + 최신 * 259 + 3) * 512] ^= 1
        media_VERDI.write_bytes(data)
        maskin = VM(Posisjon / 'build/kernel.elf', lager_medium=media_VERDI)
        try:
            maskin.Kommando('cat note.txt', ['generation-one'])
            maskin.Kommando('cat stored.txt', ['saved-from-C'])
            KR['checksum_fallback'] = maskin.LOG_POST.decode('utf-8', 'replace')
        finally:
            maskin.Lukk()
        Annet_media = Path(임시) / 'foreign.img'
        Annet_media.write_bytes(bytes([0x5a]) * (2048 * 512))
        Forrige_vare = hashlib.sha256(Annet_media.read_bytes()).hexdigest()
        maskin = VM(Posisjon / 'build/kernel.elf', lager_medium=Annet_media)
        try:
            maskin.Kommando('sync', ['Sync: -19'])
        finally:
            maskin.Lukk()
        assert hashlib.sha256(Annet_media.read_bytes()).hexdigest() == Forrige_vare
        KR['foreign_disk_unchanged'] = True
    (Posisjon / 'build/보존시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VERDI/ISO 재부팅/kontrollsum gjenopprette_status/다른 media_VERDI 비변경', flush=True)

if __name__ == '__main__':
    Utfør_kommando()
