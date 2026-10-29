#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import भ्रामक_यंत्र

स्थिती = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', स्थिती / 'साधनां/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def संपादन_करचें_मोल(यंत्र, अनुक्रमणिका_मोल):
    चलोवप = len(यंत्र.LOG_नोंद)
    यंत्र.직렬.sendall(('edit note.txt\n' + अनुक्रमणिका_मोल + '\n.save\n').encode())
    return यंत्र.기다림('jkoros> ', चलोवप)

def पाळो_दिवचो_आदेश():
    मेजप = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.निर्माण_करचें_प्रवेश(매체)
        यंत्र = भ्रामक_यंत्र(स्थिती / 'build/kernel.elf', 저장매체=매체)
        try:
            यंत्र.आदेश('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            संपादन_करचें_मोल(यंत्र, 'generation-one')
            यंत्र.आदेश('sync', ['Sync: 0'])
            संपादन_करचें_मोल(यंत्र, 'generation-two')
            यंत्र.आदेश('sync', ['Sync: 0'])
            संपादन_करचें_मोल(यंत्र, 'unsynced-three')
            मेजप['save'] = यंत्र.LOG_नोंद.decode('utf-8', 'replace')
        finally:
            यंत्र.शेवट()
        यंत्र = भ्रामक_यंत्र(स्थिती / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = यंत्र.आदेश('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            यंत्र.आदेश('cat stored.txt', ['saved-from-C'])
            मेजप['restore'] = यंत्र.LOG_नोंद.decode('utf-8', 'replace')
        finally:
            यंत्र.शेवट()
        डेटा = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', डेटा, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        डेटा[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(डेटा)
        यंत्र = भ्रामक_यंत्र(स्थिती / 'build/kernel.elf', 저장매체=매체)
        try:
            यंत्र.आदेश('cat note.txt', ['generation-one'])
            यंत्र.आदेश('cat stored.txt', ['saved-from-C'])
            मेजप['checksum_fallback'] = यंत्र.LOG_नोंद.decode('utf-8', 'replace')
        finally:
            यंत्र.शेवट()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        यंत्र = भ्रामक_यंत्र(स्थिती / 'build/kernel.elf', 저장매체=다른매체)
        try:
            यंत्र.आदेश('sync', ['Sync: -19'])
        finally:
            यंत्र.शेवट()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        मेजप['foreign_disk_unchanged'] = True
    (स्थिती / 'build/보존시험.json').write_text(json.dumps(मेजप, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_मोल/ISO 재부팅/검사합 परतून_मेळोवचें_स्थिती/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    पाळो_दिवचो_आदेश()
