#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from يختبر_مستخدم_شبكة import جهاز_ظاهري

موضع = Path(__file__).resolve().parents[1]
المواصفات = importlib.util.spec_from_file_location('وسائط_أداة', موضع / 'أدوات/فتح_تخزين_وسائط.py')
وسائط_أداة = importlib.util.module_from_spec(المواصفات)
المواصفات.loader.exec_module(وسائط_أداة)

def يحرر_قيمة(جهاز, محتوى_قيمة):
    تشغيل = len(جهاز.سجل_سجل)
    جهاز.직렬.sendall(('edit note.txt\n' + محتوى_قيمة + '\n.save\n').encode())
    return جهاز.حالة_انتظار('jkoros> ', تشغيل)

def ينفذ_أمر():
    نتيجة = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        وسائط_قيمة = Path(임시) / 'files.img'
        وسائط_أداة.فتح_إدخال(وسائط_قيمة)
        جهاز = جهاز_ظاهري(موضع / 'build/kernel.elf', تخزين_متوسط=وسائط_قيمة)
        try:
            جهاز.أمر('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            يحرر_قيمة(جهاز, 'generation-one')
            جهاز.أمر('sync', ['Sync: 0'])
            يحرر_قيمة(جهاز, 'generation-two')
            جهاز.أمر('sync', ['Sync: 0'])
            يحرر_قيمة(جهاز, 'unsynced-three')
            نتيجة['save'] = جهاز.سجل_سجل.decode('utf-8', 'replace')
        finally:
            جهاز.إغلاق()
        جهاز = جهاز_ظاهري(موضع / 'build/kernel.iso', 'iso', تخزين_متوسط=وسائط_قيمة)
        try:
            مخرجات = جهاز.أمر('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in مخرجات
            جهاز.أمر('cat stored.txt', ['saved-from-C'])
            نتيجة['restore'] = جهاز.سجل_سجل.decode('utf-8', 'replace')
        finally:
            جهاز.إغلاق()
        بيانات = bytearray(وسائط_قيمة.read_bytes())
        세대들 = [struct.unpack_from('<I', بيانات, (1 + فهرس * 259) * 512 + 4)[0] for فهرس in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        بيانات[(1 + 최신 * 259 + 3) * 512] ^= 1
        وسائط_قيمة.write_bytes(بيانات)
        جهاز = جهاز_ظاهري(موضع / 'build/kernel.elf', تخزين_متوسط=وسائط_قيمة)
        try:
            جهاز.أمر('cat note.txt', ['generation-one'])
            جهاز.أمر('cat stored.txt', ['saved-from-C'])
            نتيجة['checksum_fallback'] = جهاز.سجل_سجل.decode('utf-8', 'replace')
        finally:
            جهاز.إغلاق()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        جهاز = جهاز_ظاهري(موضع / 'build/kernel.elf', تخزين_متوسط=다른매체)
        try:
            جهاز.أمر('sync', ['Sync: -19'])
        finally:
            جهاز.إغلاق()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        نتيجة['foreign_disk_unchanged'] = True
    (موضع / 'build/보존시험.json').write_text(json.dumps(نتيجة, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE مخزن_قيمة/ISO 재부팅/مجموع_اختباري يسترد_حالة/다른 وسائط_قيمة 비변경', flush=True)

if __name__ == '__main__':
    ينفذ_أمر()
