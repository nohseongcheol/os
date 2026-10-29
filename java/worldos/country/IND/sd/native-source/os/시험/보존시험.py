#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import مجازي_مشين

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('ميڊيا_ٽول', 위치 / 'اوزار/ٺاھيو_ذخيرو_ميڊيا.py')
ميڊيا_ٽول = importlib.util.module_from_spec(명세)
명세.loader.exec_module(ميڊيا_ٽول)

def تدوين_قدر(مشين, مواد_قدر):
    هلائڻ = len(مشين.لاگ_صف)
    مشين.직렬.sendall(('edit note.txt\n' + مواد_قدر + '\n.save\n').encode())
    return مشين.기다림('jkoros> ', هلائڻ)

def تعميل_ڪرڻ_حڪم():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        ميڊيا_قدر = Path(임시) / 'files.img'
        ميڊيا_ٽول.ٺاھيو_داخلا(ميڊيا_قدر)
        مشين = مجازي_مشين(위치 / 'build/kernel.elf', 저장매체=ميڊيا_قدر)
        try:
            مشين.حڪم('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            تدوين_قدر(مشين, 'generation-one')
            مشين.حڪم('sync', ['Sync: 0'])
            تدوين_قدر(مشين, 'generation-two')
            مشين.حڪم('sync', ['Sync: 0'])
            تدوين_قدر(مشين, 'unsynced-three')
            결과['save'] = مشين.لاگ_صف.decode('utf-8', 'replace')
        finally:
            مشين.بند_ڪرڻ()
        مشين = مجازي_مشين(위치 / 'build/kernel.iso', 'iso', 저장매체=ميڊيا_قدر)
        try:
            출력 = مشين.حڪم('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            مشين.حڪم('cat stored.txt', ['saved-from-C'])
            결과['restore'] = مشين.لاگ_صف.decode('utf-8', 'replace')
        finally:
            مشين.بند_ڪرڻ()
        ڪوائف = bytearray(ميڊيا_قدر.read_bytes())
        세대들 = [struct.unpack_from('<I', ڪوائف, (1 + ابتدائي * 259) * 512 + 4)[0] for ابتدائي in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ڪوائف[(1 + 최신 * 259 + 3) * 512] ^= 1
        ميڊيا_قدر.write_bytes(ڪوائف)
        مشين = مجازي_مشين(위치 / 'build/kernel.elf', 저장매체=ميڊيا_قدر)
        try:
            مشين.حڪم('cat note.txt', ['generation-one'])
            مشين.حڪم('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = مشين.لاگ_صف.decode('utf-8', 'replace')
        finally:
            مشين.بند_ڪرڻ()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        مشين = مجازي_مشين(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            مشين.حڪم('sync', ['Sync: -19'])
        finally:
            مشين.بند_ڪرڻ()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE روڪيو_قدر/ISO 재부팅/검사합 بحال_ٿيڻ_حالت/다른 ميڊيا_قدر 비변경', flush=True)

if __name__ == '__main__':
    تعميل_ڪرڻ_حڪم()
