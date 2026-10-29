#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import virtual_maşın

yerinə_qoymaq = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', yerinə_qoymaq / 'Alətlər/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def redaktə_VALUE(maşın, Məzmun_VALUE):
    İcra_Et = len(maşın.LOG_yaz)
    maşın.직렬.sendall(('edit note.txt\n' + Məzmun_VALUE + '\n.save\n').encode())
    return maşın.gözlə_vəziyyət('jkoros> ', İcra_Et)

def icra_etmək_əmr():
    ölçü = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.yarat_daxiletmə(매체)
        maşın = virtual_maşın(yerinə_qoymaq / 'build/kernel.elf', 저장매체=매체)
        try:
            maşın.Əmr('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            redaktə_VALUE(maşın, 'generation-one')
            maşın.Əmr('sync', ['Sync: 0'])
            redaktə_VALUE(maşın, 'generation-two')
            maşın.Əmr('sync', ['Sync: 0'])
            redaktə_VALUE(maşın, 'unsynced-three')
            ölçü['save'] = maşın.LOG_yaz.decode('utf-8', 'replace')
        finally:
            maşın.Bağla()
        maşın = virtual_maşın(yerinə_qoymaq / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = maşın.Əmr('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            maşın.Əmr('cat stored.txt', ['saved-from-C'])
            ölçü['restore'] = maşın.LOG_yaz.decode('utf-8', 'replace')
        finally:
            maşın.Bağla()
        verilənlər = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', verilənlər, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        verilənlər[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(verilənlər)
        maşın = virtual_maşın(yerinə_qoymaq / 'build/kernel.elf', 저장매체=매체)
        try:
            maşın.Əmr('cat note.txt', ['generation-one'])
            maşın.Əmr('cat stored.txt', ['saved-from-C'])
            ölçü['checksum_fallback'] = maşın.LOG_yaz.decode('utf-8', 'replace')
        finally:
            maşın.Bağla()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        maşın = virtual_maşın(yerinə_qoymaq / 'build/kernel.elf', 저장매체=다른매체)
        try:
            maşın.Əmr('sync', ['Sync: -19'])
        finally:
            maşın.Bağla()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        ölçü['foreign_disk_unchanged'] = True
    (yerinə_qoymaq / 'build/보존시험.json').write_text(json.dumps(ölçü, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALUE/ISO 재부팅/검사합 bərpa_etmək_vəziyyət/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    icra_etmək_əmr()
