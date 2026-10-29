#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import віртуальны_камп_ютар

Пазіцыя = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('носьбіт_інструмент', Пазіцыя / 'Інструменты/стварыць_Сховішча_носьбіт.py')
носьбіт_інструмент = importlib.util.module_from_spec(명세)
명세.loader.exec_module(носьбіт_інструмент)

def рэдагаваць_значэнне(камп_ютар, кантэнт_значэнне):
    Выканаць = len(камп_ютар.журнал_запіс)
    камп_ютар.직렬.sendall(('edit note.txt\n' + кантэнт_значэнне + '\n.save\n').encode())
    return камп_ютар.чакае_стан('jkoros> ', Выканаць)

def выканаць_каманда():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        носьбіт_значэнне = Path(임시) / 'files.img'
        носьбіт_інструмент.стварыць_увядзенне(носьбіт_значэнне)
        камп_ютар = віртуальны_камп_ютар(Пазіцыя / 'build/kernel.elf', 저장매체=носьбіт_значэнне)
        try:
            камп_ютар.Загад('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            рэдагаваць_значэнне(камп_ютар, 'generation-one')
            камп_ютар.Загад('sync', ['Sync: 0'])
            рэдагаваць_значэнне(камп_ютар, 'generation-two')
            камп_ютар.Загад('sync', ['Sync: 0'])
            рэдагаваць_значэнне(камп_ютар, 'unsynced-three')
            결과['save'] = камп_ютар.журнал_запіс.decode('utf-8', 'replace')
        finally:
            камп_ютар.Закрыць()
        камп_ютар = віртуальны_камп_ютар(Пазіцыя / 'build/kernel.iso', 'iso', 저장매체=носьбіт_значэнне)
        try:
            Выхад = камп_ютар.Загад('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Выхад
            камп_ютар.Загад('cat stored.txt', ['saved-from-C'])
            결과['restore'] = камп_ютар.журнал_запіс.decode('utf-8', 'replace')
        finally:
            камп_ютар.Закрыць()
        дадзеныя = bytearray(носьбіт_значэнне.read_bytes())
        세대들 = [struct.unpack_from('<I', дадзеныя, (1 + індэкс * 259) * 512 + 4)[0] for індэкс in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        дадзеныя[(1 + 최신 * 259 + 3) * 512] ^= 1
        носьбіт_значэнне.write_bytes(дадзеныя)
        камп_ютар = віртуальны_камп_ютар(Пазіцыя / 'build/kernel.elf', 저장매체=носьбіт_значэнне)
        try:
            камп_ютар.Загад('cat note.txt', ['generation-one'])
            камп_ютар.Загад('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = камп_ютар.журнал_запіс.decode('utf-8', 'replace')
        finally:
            камп_ютар.Закрыць()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        камп_ютар = віртуальны_камп_ютар(Пазіцыя / 'build/kernel.elf', 저장매체=다른매체)
        try:
            камп_ютар.Загад('sync', ['Sync: -19'])
        finally:
            камп_ютар.Закрыць()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (Пазіцыя / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE сховішча_значэнне/ISO 재부팅/кантрольная_сума аднавіць_стан/다른 носьбіт_значэнне 비변경', flush=True)

if __name__ == '__main__':
    выканаць_каманда()
