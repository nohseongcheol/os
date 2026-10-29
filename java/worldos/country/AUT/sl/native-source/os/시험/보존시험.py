#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from preskusiti_uporabnik_mreža import navidezni_računalnik

Položaj = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('mediji_orodje', Položaj / 'Orodja/Ustvari_Senzor_prostora_mediji.py')
mediji_orodje = importlib.util.module_from_spec(명세)
명세.loader.exec_module(mediji_orodje)

def Uredi_VALUE(računalnik, vsebina_VALUE):
    Zaženi = len(računalnik.LOG_zapis)
    računalnik.직렬.sendall(('edit note.txt\n' + vsebina_VALUE + '\n.save\n').encode())
    return računalnik.čakalno_stanje('jkoros> ', Zaženi)

def Izvedi_ukaz():
    REZULTAT = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        mediji_VALUE = Path(임시) / 'files.img'
        mediji_orodje.Ustvari_vnos(mediji_VALUE)
        računalnik = navidezni_računalnik(Položaj / 'build/kernel.elf', Senzor_prostora_medij=mediji_VALUE)
        try:
            računalnik.Ukaz('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Uredi_VALUE(računalnik, 'generation-one')
            računalnik.Ukaz('sync', ['Sync: 0'])
            Uredi_VALUE(računalnik, 'generation-two')
            računalnik.Ukaz('sync', ['Sync: 0'])
            Uredi_VALUE(računalnik, 'unsynced-three')
            REZULTAT['save'] = računalnik.LOG_zapis.decode('utf-8', 'replace')
        finally:
            računalnik.Zapri()
        računalnik = navidezni_računalnik(Položaj / 'build/kernel.iso', 'iso', Senzor_prostora_medij=mediji_VALUE)
        try:
            Izpis = računalnik.Ukaz('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Izpis
            računalnik.Ukaz('cat stored.txt', ['saved-from-C'])
            REZULTAT['restore'] = računalnik.LOG_zapis.decode('utf-8', 'replace')
        finally:
            računalnik.Zapri()
        podatki = bytearray(mediji_VALUE.read_bytes())
        세대들 = [struct.unpack_from('<I', podatki, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        podatki[(1 + 최신 * 259 + 3) * 512] ^= 1
        mediji_VALUE.write_bytes(podatki)
        računalnik = navidezni_računalnik(Položaj / 'build/kernel.elf', Senzor_prostora_medij=mediji_VALUE)
        try:
            računalnik.Ukaz('cat note.txt', ['generation-one'])
            računalnik.Ukaz('cat stored.txt', ['saved-from-C'])
            REZULTAT['checksum_fallback'] = računalnik.LOG_zapis.decode('utf-8', 'replace')
        finally:
            računalnik.Zapri()
        Drugo_mediji = Path(임시) / 'foreign.img'
        Drugo_mediji.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(Drugo_mediji.read_bytes()).hexdigest()
        računalnik = navidezni_računalnik(Položaj / 'build/kernel.elf', Senzor_prostora_medij=Drugo_mediji)
        try:
            računalnik.Ukaz('sync', ['Sync: -19'])
        finally:
            računalnik.Zapri()
        assert hashlib.sha256(Drugo_mediji.read_bytes()).hexdigest() == 이전
        REZULTAT['foreign_disk_unchanged'] = True
    (Položaj / 'build/보존시험.json').write_text(json.dumps(REZULTAT, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/kontrolna_vsota obnoviti_stanje/다른 mediji_VALUE 비변경', flush=True)

if __name__ == '__main__':
    Izvedi_ukaz()
