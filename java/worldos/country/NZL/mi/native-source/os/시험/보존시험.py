#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import mariko_mīhini

tūranga = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('pāpāhotanga_utauta', tūranga / 'Ngā_Utauta/Waihanga_Rokiroki_pāpāhotanga.py')
pāpāhotanga_utauta = importlib.util.module_from_spec(명세)
명세.loader.exec_module(pāpāhotanga_utauta)

def whakatika_uara(mīhini, Ihirangi_uara):
    whakahaere = len(mīhini.LOG_RECORD)
    mīhini.직렬.sendall(('edit note.txt\n' + Ihirangi_uara + '\n.save\n').encode())
    return mīhini.기다림('jkoros> ', whakahaere)

def kawe_tono():
    mēhua = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        pāpāhotanga_uara = Path(임시) / 'files.img'
        pāpāhotanga_utauta.Waihanga_tāurunga(pāpāhotanga_uara)
        mīhini = mariko_mīhini(tūranga / 'build/kernel.elf', 저장매체=pāpāhotanga_uara)
        try:
            mīhini.tono('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            whakatika_uara(mīhini, 'generation-one')
            mīhini.tono('sync', ['Sync: 0'])
            whakatika_uara(mīhini, 'generation-two')
            mīhini.tono('sync', ['Sync: 0'])
            whakatika_uara(mīhini, 'unsynced-three')
            mēhua['save'] = mīhini.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mīhini.Kati()
        mīhini = mariko_mīhini(tūranga / 'build/kernel.iso', 'iso', 저장매체=pāpāhotanga_uara)
        try:
            출력 = mīhini.tono('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            mīhini.tono('cat stored.txt', ['saved-from-C'])
            mēhua['restore'] = mīhini.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mīhini.Kati()
        raraunga = bytearray(pāpāhotanga_uara.read_bytes())
        세대들 = [struct.unpack_from('<I', raraunga, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        raraunga[(1 + 최신 * 259 + 3) * 512] ^= 1
        pāpāhotanga_uara.write_bytes(raraunga)
        mīhini = mariko_mīhini(tūranga / 'build/kernel.elf', 저장매체=pāpāhotanga_uara)
        try:
            mīhini.tono('cat note.txt', ['generation-one'])
            mīhini.tono('cat stored.txt', ['saved-from-C'])
            mēhua['checksum_fallback'] = mīhini.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mīhini.Kati()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        mīhini = mariko_mīhini(tūranga / 'build/kernel.elf', 저장매체=다른매체)
        try:
            mīhini.tono('sync', ['Sync: -19'])
        finally:
            mīhini.Kati()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        mēhua['foreign_disk_unchanged'] = True
    (tūranga / 'build/보존시험.json').write_text(json.dumps(mēhua, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_uara/ISO 재부팅/검사합 whakaora_tūnga/다른 pāpāhotanga_uara 비변경', flush=True)

if __name__ == '__main__':
    kawe_tono()
