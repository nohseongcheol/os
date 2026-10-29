#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import વર્ચુઅલ_મશીન

સ્થાન = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', સ્થાન / 'ઉપકરણો/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def સંપાદન_મૂલ્ય(મશીન, સામગ્રી_મૂલ્ય):
    ચલાવો_2 = len(મશીન.લૉગ_પંક્તિ)
    મશીન.직렬.sendall(('edit note.txt\n' + સામગ્રી_મૂલ્ય + '\n.save\n').encode())
    return મશીન.પ્રતીક્ષા_સ્થિતિ('jkoros> ', ચલાવો_2)

def અમલ_કરો_આદેશ():
    પરિમાણ = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.બનાવો_પ્રવેશ(매체)
        મશીન = વર્ચુઅલ_મશીન(સ્થાન / 'build/kernel.elf', 저장매체=매체)
        try:
            મશીન.આદેશ('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            સંપાદન_મૂલ્ય(મશીન, 'generation-one')
            મશીન.આદેશ('sync', ['Sync: 0'])
            સંપાદન_મૂલ્ય(મશીન, 'generation-two')
            મશીન.આદેશ('sync', ['Sync: 0'])
            સંપાદન_મૂલ્ય(મશીન, 'unsynced-three')
            પરિમાણ['save'] = મશીન.લૉગ_પંક્તિ.decode('utf-8', 'replace')
        finally:
            મશીન.બંધ_કરો()
        મશીન = વર્ચુઅલ_મશીન(સ્થાન / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            આઉટપુટ = મશીન.આદેશ('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in આઉટપુટ
            મશીન.આદેશ('cat stored.txt', ['saved-from-C'])
            પરિમાણ['restore'] = મશીન.લૉગ_પંક્તિ.decode('utf-8', 'replace')
        finally:
            મશીન.બંધ_કરો()
        ડેટા = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', ડેટા, (1 + અનુક્રમણિકા * 259) * 512 + 4)[0] for અનુક્રમણિકા in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ડેટા[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(ડેટા)
        મશીન = વર્ચુઅલ_મશીન(સ્થાન / 'build/kernel.elf', 저장매체=매체)
        try:
            મશીન.આદેશ('cat note.txt', ['generation-one'])
            મશીન.આદેશ('cat stored.txt', ['saved-from-C'])
            પરિમાણ['checksum_fallback'] = મશીન.લૉગ_પંક્તિ.decode('utf-8', 'replace')
        finally:
            મશીન.બંધ_કરો()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        મશીન = વર્ચુઅલ_મશીન(સ્થાન / 'build/kernel.elf', 저장매체=다른매체)
        try:
            મશીન.આદેશ('sync', ['Sync: -19'])
        finally:
            મશીન.બંધ_કરો()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        પરિમાણ['foreign_disk_unchanged'] = True
    (સ્થાન / 'build/보존시험.json').write_text(json.dumps(પરિમાણ, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE સંગ્રહ_કરવો_મૂલ્ય/ISO 재부팅/ચેકસમ પુનઃપ્રાપ્ત_કરો_સ્થિતિ/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    અમલ_કરો_આદેશ()
