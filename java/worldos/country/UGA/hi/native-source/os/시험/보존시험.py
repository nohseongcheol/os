#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import वर्चुअल_मशीन

स्थान = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('मीडिया_उपकरण', स्थान / 'उपकरण/बनाएँ_संग्रहण_मीडिया.py')
मीडिया_उपकरण = importlib.util.module_from_spec(명세)
명세.loader.exec_module(मीडिया_उपकरण)

def संपादन_मान(यंत्र, सामग्री_मान):
    चलाएँ = len(यंत्र.लॉग_रिकॉर्ड)
    यंत्र.직렬.sendall(('edit note.txt\n' + सामग्री_मान + '\n.save\n').encode())
    return यंत्र.प्रतीक्षा_स्थिति('jkoros> ', चलाएँ)

def निष्पादित_करें_आदेश():
    परिणाम = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        मीडिया_मान = Path(임시) / 'files.img'
        मीडिया_उपकरण.बनाएँ_एन्ट्री(मीडिया_मान)
        यंत्र = वर्चुअल_मशीन(स्थान / 'build/kernel.elf', संग्रहण_मध्यम=मीडिया_मान)
        try:
            यंत्र.आदेश('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            संपादन_मान(यंत्र, 'generation-one')
            यंत्र.आदेश('sync', ['Sync: 0'])
            संपादन_मान(यंत्र, 'generation-two')
            यंत्र.आदेश('sync', ['Sync: 0'])
            संपादन_मान(यंत्र, 'unsynced-three')
            परिणाम['save'] = यंत्र.लॉग_रिकॉर्ड.decode('utf-8', 'replace')
        finally:
            यंत्र.बंदकरें()
        यंत्र = वर्चुअल_मशीन(स्थान / 'build/kernel.iso', 'iso', संग्रहण_मध्यम=मीडिया_मान)
        try:
            निर्गम = यंत्र.आदेश('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in निर्गम
            यंत्र.आदेश('cat stored.txt', ['saved-from-C'])
            परिणाम['restore'] = यंत्र.लॉग_रिकॉर्ड.decode('utf-8', 'replace')
        finally:
            यंत्र.बंदकरें()
        आँकड़े = bytearray(मीडिया_मान.read_bytes())
        세대들 = [struct.unpack_from('<I', आँकड़े, (1 + इंडेक्स * 259) * 512 + 4)[0] for इंडेक्स in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        आँकड़े[(1 + 최신 * 259 + 3) * 512] ^= 1
        मीडिया_मान.write_bytes(आँकड़े)
        यंत्र = वर्चुअल_मशीन(स्थान / 'build/kernel.elf', संग्रहण_मध्यम=मीडिया_मान)
        try:
            यंत्र.आदेश('cat note.txt', ['generation-one'])
            यंत्र.आदेश('cat stored.txt', ['saved-from-C'])
            परिणाम['checksum_fallback'] = यंत्र.लॉग_रिकॉर्ड.decode('utf-8', 'replace')
        finally:
            यंत्र.बंदकरें()
        अदर_मीडिया = Path(임시) / 'foreign.img'
        अदर_मीडिया.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(अदर_मीडिया.read_bytes()).hexdigest()
        यंत्र = वर्चुअल_मशीन(स्थान / 'build/kernel.elf', संग्रहण_मध्यम=अदर_मीडिया)
        try:
            यंत्र.आदेश('sync', ['Sync: -19'])
        finally:
            यंत्र.बंदकरें()
        assert hashlib.sha256(अदर_मीडिया.read_bytes()).hexdigest() == 이전
        परिणाम['foreign_disk_unchanged'] = True
    (स्थान / 'build/보존시험.json').write_text(json.dumps(परिणाम, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE स्टोर_मान/ISO 재부팅/योगफल_की_जाँच पुनर्प्राप्त_करें_अवस्था/다른 मीडिया_मान 비변경', flush=True)

if __name__ == '__main__':
    निष्पादित_करें_आदेश()
