#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import ВМ

позиція = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('носії_інструмент', позиція / 'інструменти/Створення_місце_носії.py')
носії_інструмент = importlib.util.module_from_spec(명세)
명세.loader.exec_module(носії_інструмент)

def правка_значення(комп_ютер, Вміст_значення):
    запустити = len(комп_ютер.журнал_запис)
    комп_ютер.직렬.sendall(('edit note.txt\n' + Вміст_значення + '\n.save\n').encode())
    return комп_ютер.стан_очікування('jkoros> ', запустити)

def Виконати_команда():
    результат = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        носії_значення = Path(임시) / 'files.img'
        носії_інструмент.Створення_запис(носії_значення)
        комп_ютер = ВМ(позиція / 'build/kernel.elf', місце_носій=носії_значення)
        try:
            комп_ютер.команда('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            правка_значення(комп_ютер, 'generation-one')
            комп_ютер.команда('sync', ['Sync: 0'])
            правка_значення(комп_ютер, 'generation-two')
            комп_ютер.команда('sync', ['Sync: 0'])
            правка_значення(комп_ютер, 'unsynced-three')
            результат['save'] = комп_ютер.журнал_запис.decode('utf-8', 'replace')
        finally:
            комп_ютер.Закрити()
        комп_ютер = ВМ(позиція / 'build/kernel.iso', 'iso', місце_носій=носії_значення)
        try:
            Вивід = комп_ютер.команда('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Вивід
            комп_ютер.команда('cat stored.txt', ['saved-from-C'])
            результат['restore'] = комп_ютер.журнал_запис.decode('utf-8', 'replace')
        finally:
            комп_ютер.Закрити()
        дані = bytearray(носії_значення.read_bytes())
        세대들 = [struct.unpack_from('<I', дані, (1 + індекс * 259) * 512 + 4)[0] for індекс in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        дані[(1 + 최신 * 259 + 3) * 512] ^= 1
        носії_значення.write_bytes(дані)
        комп_ютер = ВМ(позиція / 'build/kernel.elf', місце_носій=носії_значення)
        try:
            комп_ютер.команда('cat note.txt', ['generation-one'])
            комп_ютер.команда('cat stored.txt', ['saved-from-C'])
            результат['checksum_fallback'] = комп_ютер.журнал_запис.decode('utf-8', 'replace')
        finally:
            комп_ютер.Закрити()
        Інше_носії = Path(임시) / 'foreign.img'
        Інше_носії.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(Інше_носії.read_bytes()).hexdigest()
        комп_ютер = ВМ(позиція / 'build/kernel.elf', місце_носій=Інше_носії)
        try:
            комп_ютер.команда('sync', ['Sync: -19'])
        finally:
            комп_ютер.Закрити()
        assert hashlib.sha256(Інше_носії.read_bytes()).hexdigest() == 이전
        результат['foreign_disk_unchanged'] = True
    (позиція / 'build/보존시험.json').write_text(json.dumps(результат, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE сховище_значення/ISO 재부팅/контрольна_сума відновлювати_Стан/다른 носії_значення 비변경', flush=True)

if __name__ == '__main__':
    Виконати_команда()
