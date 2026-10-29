#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from тест_пользователь_сеть import VM

позиция = Path(__file__).resolve().parents[1]
спецификация = importlib.util.spec_from_file_location('носители_средство', позиция / 'инструменты/Create_Память_носители.py')
носители_средство = importlib.util.module_from_spec(спецификация)
спецификация.loader.exec_module(носители_средство)

def правка_ЗНАЧЕН(компьютер_5eb260fa, контент_ЗНАЧЕН):
    запустить = len(компьютер_5eb260fa.LOG_ЗАПИСЬ)
    компьютер_5eb260fa.직렬.sendall(('edit note.txt\n' + контент_ЗНАЧЕН + '\n.save\n').encode())
    return компьютер_5eb260fa.состояние_ожидания('jkoros> ', запустить)

def 실행():
    результат = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        носители_ЗНАЧЕН = Path(임시) / 'files.img'
        носители_средство.Create_ввод(носители_ЗНАЧЕН)
        компьютер_5eb260fa = VM(позиция / 'build/kernel.elf', Память_средний=носители_ЗНАЧЕН)
        try:
            компьютер_5eb260fa.команда('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            правка_ЗНАЧЕН(компьютер_5eb260fa, 'generation-one')
            компьютер_5eb260fa.команда('sync', ['Sync: 0'])
            правка_ЗНАЧЕН(компьютер_5eb260fa, 'generation-two')
            компьютер_5eb260fa.команда('sync', ['Sync: 0'])
            правка_ЗНАЧЕН(компьютер_5eb260fa, 'unsynced-three')
            результат['save'] = компьютер_5eb260fa.LOG_ЗАПИСЬ.decode('utf-8', 'replace')
        finally:
            компьютер_5eb260fa.Закрыть()
        компьютер_5eb260fa = VM(позиция / 'build/kernel.iso', 'iso', Память_средний=носители_ЗНАЧЕН)
        try:
            текстовыйВывод = компьютер_5eb260fa.команда('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in текстовыйВывод
            компьютер_5eb260fa.команда('cat stored.txt', ['saved-from-C'])
            результат['restore'] = компьютер_5eb260fa.LOG_ЗАПИСЬ.decode('utf-8', 'replace')
        finally:
            компьютер_5eb260fa.Закрыть()
        данные = bytearray(носители_ЗНАЧЕН.read_bytes())
        세대들 = [struct.unpack_from('<I', данные, (1 + ИНДЕКС * 259) * 512 + 4)[0] for ИНДЕКС in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        данные[(1 + 최신 * 259 + 3) * 512] ^= 1
        носители_ЗНАЧЕН.write_bytes(данные)
        компьютер_5eb260fa = VM(позиция / 'build/kernel.elf', Память_средний=носители_ЗНАЧЕН)
        try:
            компьютер_5eb260fa.команда('cat note.txt', ['generation-one'])
            компьютер_5eb260fa.команда('cat stored.txt', ['saved-from-C'])
            результат['checksum_fallback'] = компьютер_5eb260fa.LOG_ЗАПИСЬ.decode('utf-8', 'replace')
        finally:
            компьютер_5eb260fa.Закрыть()
        другое_носители = Path(임시) / 'foreign.img'
        другое_носители.write_bytes(bytes([0x5a]) * (2048 * 512))
        Назад_товар = hashlib.sha256(другое_носители.read_bytes()).hexdigest()
        компьютер_5eb260fa = VM(позиция / 'build/kernel.elf', Память_средний=другое_носители)
        try:
            компьютер_5eb260fa.команда('sync', ['Sync: -19'])
        finally:
            компьютер_5eb260fa.Закрыть()
        assert hashlib.sha256(другое_носители.read_bytes()).hexdigest() == Назад_товар
        результат['foreign_disk_unchanged'] = True
    (позиция / 'build/보존시험.json').write_text(json.dumps(результат, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_ЗНАЧЕН/ISO 재부팅/контрольная_сумма восстановить_Состояние/다른 носители_ЗНАЧЕН 비변경', flush=True)

if __name__ == '__main__':
    실행()
