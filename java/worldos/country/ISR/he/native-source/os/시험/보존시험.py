#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from נסה_משתמש_רשת import מחשב_וירטואלי

מיקום = Path(__file__).resolve().parents[1]
מפרט = importlib.util.spec_from_file_location('מדיה_כלי', מיקום / 'כלים/ליצור_אחסון_מדיה.py')
מדיה_כלי = importlib.util.module_from_spec(מפרט)
מפרט.loader.exec_module(מדיה_כלי)

def ערוך_ערך(מחשב, תוכן_ערך):
    הפעלה = len(מחשב.לרשום_שיא)
    מחשב.직렬.sendall(('edit note.txt\n' + תוכן_ערך + '\n.save\n').encode())
    return מחשב.מצב_המתנה('jkoros> ', הפעלה)

def לבצע_פקודה():
    תוצאה = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        מדיה_ערך = Path(임시) / 'files.img'
        מדיה_כלי.ליצור_ערך(מדיה_ערך)
        מחשב = מחשב_וירטואלי(מיקום / 'build/kernel.elf', אחסון_אמצעי=מדיה_ערך)
        try:
            מחשב.פקודה('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            ערוך_ערך(מחשב, 'generation-one')
            מחשב.פקודה('sync', ['Sync: 0'])
            ערוך_ערך(מחשב, 'generation-two')
            מחשב.פקודה('sync', ['Sync: 0'])
            ערוך_ערך(מחשב, 'unsynced-three')
            תוצאה['save'] = מחשב.לרשום_שיא.decode('utf-8', 'replace')
        finally:
            מחשב.סגירה()
        מחשב = מחשב_וירטואלי(מיקום / 'build/kernel.iso', 'iso', אחסון_אמצעי=מדיה_ערך)
        try:
            פלטטקסט = מחשב.פקודה('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in פלטטקסט
            מחשב.פקודה('cat stored.txt', ['saved-from-C'])
            תוצאה['restore'] = מחשב.לרשום_שיא.decode('utf-8', 'replace')
        finally:
            מחשב.סגירה()
        נתונים = bytearray(מדיה_ערך.read_bytes())
        세대들 = [struct.unpack_from('<I', נתונים, (1 + מדד * 259) * 512 + 4)[0] for מדד in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        נתונים[(1 + 최신 * 259 + 3) * 512] ^= 1
        מדיה_ערך.write_bytes(נתונים)
        מחשב = מחשב_וירטואלי(מיקום / 'build/kernel.elf', אחסון_אמצעי=מדיה_ערך)
        try:
            מחשב.פקודה('cat note.txt', ['generation-one'])
            מחשב.פקודה('cat stored.txt', ['saved-from-C'])
            תוצאה['checksum_fallback'] = מחשב.לרשום_שיא.decode('utf-8', 'replace')
        finally:
            מחשב.סגירה()
        אחר_מדיה = Path(임시) / 'foreign.img'
        אחר_מדיה.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(אחר_מדיה.read_bytes()).hexdigest()
        מחשב = מחשב_וירטואלי(מיקום / 'build/kernel.elf', אחסון_אמצעי=אחר_מדיה)
        try:
            מחשב.פקודה('sync', ['Sync: -19'])
        finally:
            מחשב.סגירה()
        assert hashlib.sha256(אחר_מדיה.read_bytes()).hexdigest() == 이전
        תוצאה['foreign_disk_unchanged'] = True
    (מיקום / 'build/보존시험.json').write_text(json.dumps(תוצאה, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE מאגר_ערך/ISO 재부팅/בדיקת_סיכום לשחזר_מצב/다른 מדיה_ערך 비변경', flush=True)

if __name__ == '__main__':
    לבצע_פקודה()
