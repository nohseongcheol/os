#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import अवास्तविक_मेशिन

स्थिति = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', स्थिति / 'उपकरणहरू/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def सम्पादन_गर्नुहोस्_मान(मेशिन, सामग्री_मान):
    चलाउनुहोस् = len(मेशिन.लग_रेकर्ड)
    मेशिन.직렬.sendall(('edit note.txt\n' + सामग्री_मान + '\n.save\n').encode())
    return मेशिन.기다림('jkoros> ', चलाउनुहोस्)

def कार्यान्वयन_गर्नुहोस्_आदेश():
    मापन = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.सिर्जना_प्रविष्टि(매체)
        मेशिन = अवास्तविक_मेशिन(स्थिति / 'build/kernel.elf', 저장매체=매체)
        try:
            मेशिन.आदेश('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            सम्पादन_गर्नुहोस्_मान(मेशिन, 'generation-one')
            मेशिन.आदेश('sync', ['Sync: 0'])
            सम्पादन_गर्नुहोस्_मान(मेशिन, 'generation-two')
            मेशिन.आदेश('sync', ['Sync: 0'])
            सम्पादन_गर्नुहोस्_मान(मेशिन, 'unsynced-three')
            मापन['save'] = मेशिन.लग_रेकर्ड.decode('utf-8', 'replace')
        finally:
            मेशिन.बन्दगर्नुहोस्()
        मेशिन = अवास्तविक_मेशिन(स्थिति / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = मेशिन.आदेश('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            मेशिन.आदेश('cat stored.txt', ['saved-from-C'])
            मापन['restore'] = मेशिन.लग_रेकर्ड.decode('utf-8', 'replace')
        finally:
            मेशिन.बन्दगर्नुहोस्()
        लगत = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', लगत, (1 + अनुक्रमणिका * 259) * 512 + 4)[0] for अनुक्रमणिका in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        लगत[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(लगत)
        मेशिन = अवास्तविक_मेशिन(स्थिति / 'build/kernel.elf', 저장매체=매체)
        try:
            मेशिन.आदेश('cat note.txt', ['generation-one'])
            मेशिन.आदेश('cat stored.txt', ['saved-from-C'])
            मापन['checksum_fallback'] = मेशिन.लग_रेकर्ड.decode('utf-8', 'replace')
        finally:
            मेशिन.बन्दगर्नुहोस्()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        मेशिन = अवास्तविक_मेशिन(स्थिति / 'build/kernel.elf', 저장매체=다른매체)
        try:
            मेशिन.आदेश('sync', ['Sync: -19'])
        finally:
            मेशिन.बन्दगर्नुहोस्()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        मापन['foreign_disk_unchanged'] = True
    (स्थिति / 'build/보존시험.json').write_text(json.dumps(मापन, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE भण्डार_गर्नुहोस्_मान/ISO 재부팅/검사합 पुन_प्राप्त_गर्नुहोस्_स्थिति/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    कार्यान्वयन_गर्नुहोस्_आदेश()
