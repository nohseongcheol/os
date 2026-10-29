#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import അയഥാര്_ഥ_മെഷീൻ

സ്ഥാനം = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', സ്ഥാനം / 'ഉപകരണങ്ങൾ/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, ഉള്ളടക്കം_മൂല്യം):
    നടപ്പിലാക്കുക = len(മെഷീൻ.ലോഗ്_രേഖ)
    മെഷീൻ.직렬.sendall(('edit note.txt\n' + ഉള്ളടക്കം_മൂല്യം + '\n.save\n').encode())
    return മെഷീൻ.കാക്കുക_അവസ്ഥ('jkoros> ', നടപ്പിലാക്കുക)

def നടപ്പാക്കുക_കമാന്_ഡ്():
    അളവ് = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.സൃഷ്_ടിക്കുക_എന്_ട്രി(매체)
        മെഷീൻ = അയഥാര്_ഥ_മെഷീൻ(സ്ഥാനം / 'build/kernel.elf', 저장매체=매체)
        try:
            മെഷീൻ.ആജ്ഞ('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, 'generation-one')
            മെഷീൻ.ആജ്ഞ('sync', ['Sync: 0'])
            ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, 'generation-two')
            മെഷീൻ.ആജ്ഞ('sync', ['Sync: 0'])
            ചിട്ടപ്പെടുത്തല്_മൂല്യം(മെഷീൻ, 'unsynced-three')
            അളവ്['save'] = മെഷീൻ.ലോഗ്_രേഖ.decode('utf-8', 'replace')
        finally:
            മെഷീൻ.അടയ്ക്കു()
        മെഷീൻ = അയഥാര്_ഥ_മെഷീൻ(സ്ഥാനം / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            ഫലം = മെഷീൻ.ആജ്ഞ('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in ഫലം
            മെഷീൻ.ആജ്ഞ('cat stored.txt', ['saved-from-C'])
            അളവ്['restore'] = മെഷീൻ.ലോഗ്_രേഖ.decode('utf-8', 'replace')
        finally:
            മെഷീൻ.അടയ്ക്കു()
        ഡാറ്റാ = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', ഡാറ്റാ, (1 + സൂചിക * 259) * 512 + 4)[0] for സൂചിക in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ഡാറ്റാ[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(ഡാറ്റാ)
        മെഷീൻ = അയഥാര്_ഥ_മെഷീൻ(സ്ഥാനം / 'build/kernel.elf', 저장매체=매체)
        try:
            മെഷീൻ.ആജ്ഞ('cat note.txt', ['generation-one'])
            മെഷീൻ.ആജ്ഞ('cat stored.txt', ['saved-from-C'])
            അളവ്['checksum_fallback'] = മെഷീൻ.ലോഗ്_രേഖ.decode('utf-8', 'replace')
        finally:
            മെഷീൻ.അടയ്ക്കു()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        മെഷീൻ = അയഥാര്_ഥ_മെഷീൻ(സ്ഥാനം / 'build/kernel.elf', 저장매체=다른매체)
        try:
            മെഷീൻ.ആജ്ഞ('sync', ['Sync: -19'])
        finally:
            മെഷീൻ.അടയ്ക്കു()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        അളവ്['foreign_disk_unchanged'] = True
    (സ്ഥാനം / 'build/보존시험.json').write_text(json.dumps(അളവ്, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE സ്_റ്റോർ_മൂല്യം/ISO 재부팅/검사합 വീണ്ടെടുക്കുക_അവസ്ഥ/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    നടപ്പാക്കുക_കമാന്_ഡ്()
