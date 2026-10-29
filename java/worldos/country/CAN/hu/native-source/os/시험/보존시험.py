#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from teszt_felhasználó_hálózat import VM

Pozíció = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('Multimédia_eszköz', Pozíció / 'Eszközök/készít_tár_Multimédia.py')
Multimédia_eszköz = importlib.util.module_from_spec(명세)
명세.loader.exec_module(Multimédia_eszköz)

def szerkeszt_ÉRTÉK(gép, Tartalom_ÉRTÉK):
    Futtatás = len(gép.LOG_REKORD)
    gép.직렬.sendall(('edit note.txt\n' + Tartalom_ÉRTÉK + '\n.save\n').encode())
    return gép.várakozóállapot('jkoros> ', Futtatás)

def végrehajt_parancs():
    KR = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        Multimédia_ÉRTÉK = Path(임시) / 'files.img'
        Multimédia_eszköz.készít_bejegyzés(Multimédia_ÉRTÉK)
        gép = VM(Pozíció / 'build/kernel.elf', tár_Közepes=Multimédia_ÉRTÉK)
        try:
            gép.Parancs('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            szerkeszt_ÉRTÉK(gép, 'generation-one')
            gép.Parancs('sync', ['Sync: 0'])
            szerkeszt_ÉRTÉK(gép, 'generation-two')
            gép.Parancs('sync', ['Sync: 0'])
            szerkeszt_ÉRTÉK(gép, 'unsynced-three')
            KR['save'] = gép.LOG_REKORD.decode('utf-8', 'replace')
        finally:
            gép.Bezárás()
        gép = VM(Pozíció / 'build/kernel.iso', 'iso', tár_Közepes=Multimédia_ÉRTÉK)
        try:
            Kimenet = gép.Parancs('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Kimenet
            gép.Parancs('cat stored.txt', ['saved-from-C'])
            KR['restore'] = gép.LOG_REKORD.decode('utf-8', 'replace')
        finally:
            gép.Bezárás()
        adat = bytearray(Multimédia_ÉRTÉK.read_bytes())
        세대들 = [struct.unpack_from('<I', adat, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        adat[(1 + 최신 * 259 + 3) * 512] ^= 1
        Multimédia_ÉRTÉK.write_bytes(adat)
        gép = VM(Pozíció / 'build/kernel.elf', tár_Közepes=Multimédia_ÉRTÉK)
        try:
            gép.Parancs('cat note.txt', ['generation-one'])
            gép.Parancs('cat stored.txt', ['saved-from-C'])
            KR['checksum_fallback'] = gép.LOG_REKORD.decode('utf-8', 'replace')
        finally:
            gép.Bezárás()
        Egyéb_Multimédia = Path(임시) / 'foreign.img'
        Egyéb_Multimédia.write_bytes(bytes([0x5a]) * (2048 * 512))
        Előző_cikk = hashlib.sha256(Egyéb_Multimédia.read_bytes()).hexdigest()
        gép = VM(Pozíció / 'build/kernel.elf', tár_Közepes=Egyéb_Multimédia)
        try:
            gép.Parancs('sync', ['Sync: -19'])
        finally:
            gép.Bezárás()
        assert hashlib.sha256(Egyéb_Multimédia.read_bytes()).hexdigest() == Előző_cikk
        KR['foreign_disk_unchanged'] = True
    (Pozíció / 'build/보존시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE tár_ÉRTÉK/ISO 재부팅/ellenőrzőösszeg helyreállít_Állapot/다른 Multimédia_ÉRTÉK 비변경', flush=True)

if __name__ == '__main__':
    végrehajt_parancs()
