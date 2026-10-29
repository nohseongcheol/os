#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import مجازی_دستگاه

مرتب_کردن = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', مرتب_کردن / 'ابزارها/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def ویرایش_مقدار(دستگاه, محتوا_مقدار):
    اجرا_2 = len(دستگاه.واقعه_نگار_ردیف)
    دستگاه.직렬.sendall(('edit note.txt\n' + محتوا_مقدار + '\n.save\n').encode())
    return دستگاه.منتظر_ماندن_وضعیت('jkoros> ', اجرا_2)

def اجرا_فرمان():
    سنجش = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.ایجاد_ورودی(매체)
        دستگاه = مجازی_دستگاه(مرتب_کردن / 'build/kernel.elf', 저장매체=매체)
        try:
            دستگاه.فرمان('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            ویرایش_مقدار(دستگاه, 'generation-one')
            دستگاه.فرمان('sync', ['Sync: 0'])
            ویرایش_مقدار(دستگاه, 'generation-two')
            دستگاه.فرمان('sync', ['Sync: 0'])
            ویرایش_مقدار(دستگاه, 'unsynced-three')
            سنجش['save'] = دستگاه.واقعه_نگار_ردیف.decode('utf-8', 'replace')
        finally:
            دستگاه.بستن()
        دستگاه = مجازی_دستگاه(مرتب_کردن / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            خروجی = دستگاه.فرمان('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in خروجی
            دستگاه.فرمان('cat stored.txt', ['saved-from-C'])
            سنجش['restore'] = دستگاه.واقعه_نگار_ردیف.decode('utf-8', 'replace')
        finally:
            دستگاه.بستن()
        داده_ها = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', داده_ها, (1 + فهرست * 259) * 512 + 4)[0] for فهرست in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        داده_ها[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(داده_ها)
        دستگاه = مجازی_دستگاه(مرتب_کردن / 'build/kernel.elf', 저장매체=매체)
        try:
            دستگاه.فرمان('cat note.txt', ['generation-one'])
            دستگاه.فرمان('cat stored.txt', ['saved-from-C'])
            سنجش['checksum_fallback'] = دستگاه.واقعه_نگار_ردیف.decode('utf-8', 'replace')
        finally:
            دستگاه.بستن()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        دستگاه = مجازی_دستگاه(مرتب_کردن / 'build/kernel.elf', 저장매체=다른매체)
        try:
            دستگاه.فرمان('sync', ['Sync: -19'])
        finally:
            دستگاه.بستن()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        سنجش['foreign_disk_unchanged'] = True
    (مرتب_کردن / 'build/보존시험.json').write_text(json.dumps(سنجش, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE ذخیره_مقدار/ISO 재부팅/مجموع_مقابله_ای بازیابی_وضعیت/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    اجرا_فرمان()
