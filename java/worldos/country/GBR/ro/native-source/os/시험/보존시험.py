#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import VM

Poziție = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('suport_fizic_instrument', Poziție / 'Instrumente/crea_Stocare_suport_fizic.py')
suport_fizic_instrument = importlib.util.module_from_spec(명세)
명세.loader.exec_module(suport_fizic_instrument)

def edita_VALUE(mașină, Conținut_VALUE):
    Pornește = len(mașină.LOG_RECORD)
    mașină.직렬.sendall(('edit note.txt\n' + Conținut_VALUE + '\n.save\n').encode())
    return mașină.stare_de_așteptare('jkoros> ', Pornește)

def executa_comandă():
    KR = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        suport_fizic_VALUE = Path(임시) / 'files.img'
        suport_fizic_instrument.crea_intrare(suport_fizic_VALUE)
        mașină = VM(Poziție / 'build/kernel.elf', Stocare_Mediu=suport_fizic_VALUE)
        try:
            mașină.Comandă('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            edita_VALUE(mașină, 'generation-one')
            mașină.Comandă('sync', ['Sync: 0'])
            edita_VALUE(mașină, 'generation-two')
            mașină.Comandă('sync', ['Sync: 0'])
            edita_VALUE(mașină, 'unsynced-three')
            KR['save'] = mașină.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mașină.Închide()
        mașină = VM(Poziție / 'build/kernel.iso', 'iso', Stocare_Mediu=suport_fizic_VALUE)
        try:
            Rezultat = mașină.Comandă('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Rezultat
            mașină.Comandă('cat stored.txt', ['saved-from-C'])
            KR['restore'] = mașină.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mașină.Închide()
        date = bytearray(suport_fizic_VALUE.read_bytes())
        세대들 = [struct.unpack_from('<I', date, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        date[(1 + 최신 * 259 + 3) * 512] ^= 1
        suport_fizic_VALUE.write_bytes(date)
        mașină = VM(Poziție / 'build/kernel.elf', Stocare_Mediu=suport_fizic_VALUE)
        try:
            mașină.Comandă('cat note.txt', ['generation-one'])
            mașină.Comandă('cat stored.txt', ['saved-from-C'])
            KR['checksum_fallback'] = mașină.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mașină.Închide()
        Altele_suport_fizic = Path(임시) / 'foreign.img'
        Altele_suport_fizic.write_bytes(bytes([0x5a]) * (2048 * 512))
        Anteriorul_element = hashlib.sha256(Altele_suport_fizic.read_bytes()).hexdigest()
        mașină = VM(Poziție / 'build/kernel.elf', Stocare_Mediu=Altele_suport_fizic)
        try:
            mașină.Comandă('sync', ['Sync: -19'])
        finally:
            mașină.Închide()
        assert hashlib.sha256(Altele_suport_fizic.read_bytes()).hexdigest() == Anteriorul_element
        KR['foreign_disk_unchanged'] = True
    (Poziție / 'build/보존시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/sumă_de_verificare recupera_Stare/다른 suport_fizic_VALUE 비변경', flush=True)

if __name__ == '__main__':
    executa_comandă()
