#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import виртуелен_машина

Позиција = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', Позиција / 'Алатки/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def уреди_VALUE(машина, Содржина_VALUE):
    Изврши_2 = len(машина.LOG_ред)
    машина.직렬.sendall(('edit note.txt\n' + Содржина_VALUE + '\n.save\n').encode())
    return машина.почекај_статус('jkoros> ', Изврши_2)

def Изврши_наредба():
    мерка = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.Create_внес(매체)
        машина = виртуелен_машина(Позиција / 'build/kernel.elf', 저장매체=매체)
        try:
            машина.Команда('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            уреди_VALUE(машина, 'generation-one')
            машина.Команда('sync', ['Sync: 0'])
            уреди_VALUE(машина, 'generation-two')
            машина.Команда('sync', ['Sync: 0'])
            уреди_VALUE(машина, 'unsynced-three')
            мерка['save'] = машина.LOG_ред.decode('utf-8', 'replace')
        finally:
            машина.Затвори()
        машина = виртуелен_машина(Позиција / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = машина.Команда('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            машина.Команда('cat stored.txt', ['saved-from-C'])
            мерка['restore'] = машина.LOG_ред.decode('utf-8', 'replace')
        finally:
            машина.Затвори()
        податоци = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', податоци, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        податоци[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(податоци)
        машина = виртуелен_машина(Позиција / 'build/kernel.elf', 저장매체=매체)
        try:
            машина.Команда('cat note.txt', ['generation-one'])
            машина.Команда('cat stored.txt', ['saved-from-C'])
            мерка['checksum_fallback'] = машина.LOG_ред.decode('utf-8', 'replace')
        finally:
            машина.Затвори()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        машина = виртуелен_машина(Позиција / 'build/kernel.elf', 저장매체=다른매체)
        try:
            машина.Команда('sync', ['Sync: -19'])
        finally:
            машина.Затвори()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        мерка['foreign_disk_unchanged'] = True
    (Позиција / 'build/보존시험.json').write_text(json.dumps(мерка, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/контролна_сума опоравува_статус/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    Изврши_наредба()
