#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import виртуална_машина

Позиция = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', Позиция / 'Инструменти/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def редакция_стойност(машина, Съдържание_стойност):
    Стартиране = len(машина.регистрирам_запис)
    машина.직렬.sendall(('edit note.txt\n' + Съдържание_стойност + '\n.save\n').encode())
    return машина.състояние_на_изчакване('jkoros> ', Стартиране)

def изпълнявам_команда():
    РЕЗУЛТАТ = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.Създаване_запис(매체)
        машина = виртуална_машина(Позиция / 'build/kernel.elf', Памет_среда=매체)
        try:
            машина.Команда('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            редакция_стойност(машина, 'generation-one')
            машина.Команда('sync', ['Sync: 0'])
            редакция_стойност(машина, 'generation-two')
            машина.Команда('sync', ['Sync: 0'])
            редакция_стойност(машина, 'unsynced-three')
            РЕЗУЛТАТ['save'] = машина.регистрирам_запис.decode('utf-8', 'replace')
        finally:
            машина.Затворен()
        машина = виртуална_машина(Позиция / 'build/kernel.iso', 'iso', Памет_среда=매체)
        try:
            Изход = машина.Команда('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Изход
            машина.Команда('cat stored.txt', ['saved-from-C'])
            РЕЗУЛТАТ['restore'] = машина.регистрирам_запис.decode('utf-8', 'replace')
        finally:
            машина.Затворен()
        данни = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', данни, (1 + индекс * 259) * 512 + 4)[0] for индекс in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        данни[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(данни)
        машина = виртуална_машина(Позиция / 'build/kernel.elf', Памет_среда=매체)
        try:
            машина.Команда('cat note.txt', ['generation-one'])
            машина.Команда('cat stored.txt', ['saved-from-C'])
            РЕЗУЛТАТ['checksum_fallback'] = машина.регистрирам_запис.decode('utf-8', 'replace')
        finally:
            машина.Затворен()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        машина = виртуална_машина(Позиция / 'build/kernel.elf', Памет_среда=다른매체)
        try:
            машина.Команда('sync', ['Sync: -19'])
        finally:
            машина.Затворен()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        РЕЗУЛТАТ['foreign_disk_unchanged'] = True
    (Позиция / 'build/보존시험.json').write_text(json.dumps(РЕЗУЛТАТ, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE хранилище_стойност/ISO 재부팅/контролна_сума възстановявам_Състояние/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    изпълнявам_команда()
