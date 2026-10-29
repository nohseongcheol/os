#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from test_użytkownik_sieć import maszyna_wirtualna

pozycja = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('nośnik_narzędzie', pozycja / 'narzędzia/Twórca_Pamięć_nośnik.py')
nośnik_narzędzie = importlib.util.module_from_spec(명세)
명세.loader.exec_module(nośnik_narzędzie)

def Edytuj_WARTOŚĆ(maszyna, treść_WARTOŚĆ_cb0f2404):
    Uruchom_2 = len(maszyna.LOG_zapis)
    maszyna.직렬.sendall(('edit note.txt\n' + treść_WARTOŚĆ_cb0f2404 + '\n.save\n').encode())
    return maszyna.stan_oczekiwania('jkoros> ', Uruchom_2)

def Wykonaj_polecenie():
    WYNIK = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        nośnik_WARTOŚĆ = Path(임시) / 'files.img'
        nośnik_narzędzie.Twórca_wpis(nośnik_WARTOŚĆ)
        maszyna = maszyna_wirtualna(pozycja / 'build/kernel.elf', Pamięć_nośnik=nośnik_WARTOŚĆ)
        try:
            maszyna.polecenie('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Edytuj_WARTOŚĆ(maszyna, 'generation-one')
            maszyna.polecenie('sync', ['Sync: 0'])
            Edytuj_WARTOŚĆ(maszyna, 'generation-two')
            maszyna.polecenie('sync', ['Sync: 0'])
            Edytuj_WARTOŚĆ(maszyna, 'unsynced-three')
            WYNIK['save'] = maszyna.LOG_zapis.decode('utf-8', 'replace')
        finally:
            maszyna.Zamknięte()
        maszyna = maszyna_wirtualna(pozycja / 'build/kernel.iso', 'iso', Pamięć_nośnik=nośnik_WARTOŚĆ)
        try:
            pozycja_wyjścia = maszyna.polecenie('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in pozycja_wyjścia
            maszyna.polecenie('cat stored.txt', ['saved-from-C'])
            WYNIK['restore'] = maszyna.LOG_zapis.decode('utf-8', 'replace')
        finally:
            maszyna.Zamknięte()
        dane = bytearray(nośnik_WARTOŚĆ.read_bytes())
        세대들 = [struct.unpack_from('<I', dane, (1 + INDEKS * 259) * 512 + 4)[0] for INDEKS in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        dane[(1 + 최신 * 259 + 3) * 512] ^= 1
        nośnik_WARTOŚĆ.write_bytes(dane)
        maszyna = maszyna_wirtualna(pozycja / 'build/kernel.elf', Pamięć_nośnik=nośnik_WARTOŚĆ)
        try:
            maszyna.polecenie('cat note.txt', ['generation-one'])
            maszyna.polecenie('cat stored.txt', ['saved-from-C'])
            WYNIK['checksum_fallback'] = maszyna.LOG_zapis.decode('utf-8', 'replace')
        finally:
            maszyna.Zamknięte()
        Inne_nośnik = Path(임시) / 'foreign.img'
        Inne_nośnik.write_bytes(bytes([0x5a]) * (2048 * 512))
        Wstecz_towar = hashlib.sha256(Inne_nośnik.read_bytes()).hexdigest()
        maszyna = maszyna_wirtualna(pozycja / 'build/kernel.elf', Pamięć_nośnik=Inne_nośnik)
        try:
            maszyna.polecenie('sync', ['Sync: -19'])
        finally:
            maszyna.Zamknięte()
        assert hashlib.sha256(Inne_nośnik.read_bytes()).hexdigest() == Wstecz_towar
        WYNIK['foreign_disk_unchanged'] = True
    (pozycja / 'build/보존시험.json').write_text(json.dumps(WYNIK, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_WARTOŚĆ/ISO 재부팅/suma_kontrolna odzyskać_Stan/다른 nośnik_WARTOŚĆ 비변경', flush=True)

if __name__ == '__main__':
    Wykonaj_polecenie()
