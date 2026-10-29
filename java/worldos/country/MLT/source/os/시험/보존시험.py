#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import virtwali_kompjuter

pożizzjoni = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', pożizzjoni / 'Għodod/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def editja_VALUE(kompjuter, Kontenut_VALUE):
    serje = len(kompjuter.LOG_RECORD)
    kompjuter.직렬.sendall(('edit note.txt\n' + Kontenut_VALUE + '\n.save\n').encode())
    return kompjuter.기다림('jkoros> ', serje)

def eżegwixxa_kmand():
    miżura = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.ħalaq_entrata(매체)
        kompjuter = virtwali_kompjuter(pożizzjoni / 'build/kernel.elf', 저장매체=매체)
        try:
            kompjuter.kmand('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            editja_VALUE(kompjuter, 'generation-one')
            kompjuter.kmand('sync', ['Sync: 0'])
            editja_VALUE(kompjuter, 'generation-two')
            kompjuter.kmand('sync', ['Sync: 0'])
            editja_VALUE(kompjuter, 'unsynced-three')
            miżura['save'] = kompjuter.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            kompjuter.agħlaq()
        kompjuter = virtwali_kompjuter(pożizzjoni / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = kompjuter.kmand('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            kompjuter.kmand('cat stored.txt', ['saved-from-C'])
            miżura['restore'] = kompjuter.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            kompjuter.agħlaq()
        data = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', data, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        data[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(data)
        kompjuter = virtwali_kompjuter(pożizzjoni / 'build/kernel.elf', 저장매체=매체)
        try:
            kompjuter.kmand('cat note.txt', ['generation-one'])
            kompjuter.kmand('cat stored.txt', ['saved-from-C'])
            miżura['checksum_fallback'] = kompjuter.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            kompjuter.agħlaq()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        kompjuter = virtwali_kompjuter(pożizzjoni / 'build/kernel.elf', 저장매체=다른매체)
        try:
            kompjuter.kmand('sync', ['Sync: -19'])
        finally:
            kompjuter.agħlaq()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        miżura['foreign_disk_unchanged'] = True
    (pożizzjoni / 'build/보존시험.json').write_text(json.dumps(miżura, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/검사합 rkupra_stat/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    eżegwixxa_kmand()
