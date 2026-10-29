#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from δοκιμή_χρήστης_δίκτυο import εικονική_μηχανή

Θέση = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('μέσα_εργαλείο', Θέση / 'Εργαλεία/ανοίγω_Χώρος_αποθήκευσης_μέσα.py')
μέσα_εργαλείο = importlib.util.module_from_spec(명세)
명세.loader.exec_module(μέσα_εργαλείο)

def Τροποποίησε_τιμή(υπολογιστής_5eb260fa, Περιεχόμενο_τιμή):
    Εκτέλεση_2 = len(υπολογιστής_5eb260fa.καταγράφω_ρεκόρ)
    υπολογιστής_5eb260fa.직렬.sendall(('edit note.txt\n' + Περιεχόμενο_τιμή + '\n.save\n').encode())
    return υπολογιστής_5eb260fa.κατάσταση_αναμονής('jkoros> ', Εκτέλεση_2)

def εκτελώ_εντολή():
    μέτρηση = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        μέσα_τιμή = Path(임시) / 'files.img'
        μέσα_εργαλείο.ανοίγω_καταχώρηση(μέσα_τιμή)
        υπολογιστής_5eb260fa = εικονική_μηχανή(Θέση / 'build/kernel.elf', Χώρος_αποθήκευσης_μέσο=μέσα_τιμή)
        try:
            υπολογιστής_5eb260fa.Εντολή('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Τροποποίησε_τιμή(υπολογιστής_5eb260fa, 'generation-one')
            υπολογιστής_5eb260fa.Εντολή('sync', ['Sync: 0'])
            Τροποποίησε_τιμή(υπολογιστής_5eb260fa, 'generation-two')
            υπολογιστής_5eb260fa.Εντολή('sync', ['Sync: 0'])
            Τροποποίησε_τιμή(υπολογιστής_5eb260fa, 'unsynced-three')
            μέτρηση['save'] = υπολογιστής_5eb260fa.καταγράφω_ρεκόρ.decode('utf-8', 'replace')
        finally:
            υπολογιστής_5eb260fa.Κλείσιμο()
        υπολογιστής_5eb260fa = εικονική_μηχανή(Θέση / 'build/kernel.iso', 'iso', Χώρος_αποθήκευσης_μέσο=μέσα_τιμή)
        try:
            Έξοδος = υπολογιστής_5eb260fa.Εντολή('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Έξοδος
            υπολογιστής_5eb260fa.Εντολή('cat stored.txt', ['saved-from-C'])
            μέτρηση['restore'] = υπολογιστής_5eb260fa.καταγράφω_ρεκόρ.decode('utf-8', 'replace')
        finally:
            υπολογιστής_5eb260fa.Κλείσιμο()
        δεδομένα = bytearray(μέσα_τιμή.read_bytes())
        세대들 = [struct.unpack_from('<I', δεδομένα, (1 + Ευρετήριο * 259) * 512 + 4)[0] for Ευρετήριο in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        δεδομένα[(1 + 최신 * 259 + 3) * 512] ^= 1
        μέσα_τιμή.write_bytes(δεδομένα)
        υπολογιστής_5eb260fa = εικονική_μηχανή(Θέση / 'build/kernel.elf', Χώρος_αποθήκευσης_μέσο=μέσα_τιμή)
        try:
            υπολογιστής_5eb260fa.Εντολή('cat note.txt', ['generation-one'])
            υπολογιστής_5eb260fa.Εντολή('cat stored.txt', ['saved-from-C'])
            μέτρηση['checksum_fallback'] = υπολογιστής_5eb260fa.καταγράφω_ρεκόρ.decode('utf-8', 'replace')
        finally:
            υπολογιστής_5eb260fa.Κλείσιμο()
        Άλλο_μέσα = Path(임시) / 'foreign.img'
        Άλλο_μέσα.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(Άλλο_μέσα.read_bytes()).hexdigest()
        υπολογιστής_5eb260fa = εικονική_μηχανή(Θέση / 'build/kernel.elf', Χώρος_αποθήκευσης_μέσο=Άλλο_μέσα)
        try:
            υπολογιστής_5eb260fa.Εντολή('sync', ['Sync: -19'])
        finally:
            υπολογιστής_5eb260fa.Κλείσιμο()
        assert hashlib.sha256(Άλλο_μέσα.read_bytes()).hexdigest() == 이전
        μέτρηση['foreign_disk_unchanged'] = True
    (Θέση / 'build/보존시험.json').write_text(json.dumps(μέτρηση, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE αποθηκεύω_τιμή/ISO 재부팅/άθροισμα_ελέγχου αποκαθιστώ_Κατάσταση/다른 μέσα_τιμή 비변경', flush=True)

if __name__ == '__main__':
    εκτελώ_εντολή()
