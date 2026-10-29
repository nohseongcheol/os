#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import fíorúil_meaisín

suíomh = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', suíomh / 'Uirlisí/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def cuir_in_eagar_VALUE(meaisín, Inneachar_VALUE):
    Rith_2 = len(meaisín.LOG_ró)
    meaisín.직렬.sendall(('edit note.txt\n' + Inneachar_VALUE + '\n.save\n').encode())
    return meaisín.기다림('jkoros> ', Rith_2)

def Rith_ordú():
    tomhas = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.Create_iontráil(매체)
        meaisín = fíorúil_meaisín(suíomh / 'build/kernel.elf', 저장매체=매체)
        try:
            meaisín.Ordú('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            cuir_in_eagar_VALUE(meaisín, 'generation-one')
            meaisín.Ordú('sync', ['Sync: 0'])
            cuir_in_eagar_VALUE(meaisín, 'generation-two')
            meaisín.Ordú('sync', ['Sync: 0'])
            cuir_in_eagar_VALUE(meaisín, 'unsynced-three')
            tomhas['save'] = meaisín.LOG_ró.decode('utf-8', 'replace')
        finally:
            meaisín.Dún()
        meaisín = fíorúil_meaisín(suíomh / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            Aschur = meaisín.Ordú('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Aschur
            meaisín.Ordú('cat stored.txt', ['saved-from-C'])
            tomhas['restore'] = meaisín.LOG_ró.decode('utf-8', 'replace')
        finally:
            meaisín.Dún()
        sonraí = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', sonraí, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        sonraí[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(sonraí)
        meaisín = fíorúil_meaisín(suíomh / 'build/kernel.elf', 저장매체=매체)
        try:
            meaisín.Ordú('cat note.txt', ['generation-one'])
            meaisín.Ordú('cat stored.txt', ['saved-from-C'])
            tomhas['checksum_fallback'] = meaisín.LOG_ró.decode('utf-8', 'replace')
        finally:
            meaisín.Dún()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        meaisín = fíorúil_meaisín(suíomh / 'build/kernel.elf', 저장매체=다른매체)
        try:
            meaisín.Ordú('sync', ['Sync: -19'])
        finally:
            meaisín.Dún()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        tomhas['foreign_disk_unchanged'] = True
    (suíomh / 'build/보존시험.json').write_text(json.dumps(tomhas, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/suim_seiceála athshlánaigh_staid/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    Rith_ordú()
