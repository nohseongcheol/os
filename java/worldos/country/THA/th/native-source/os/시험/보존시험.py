#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from การทดสอบ_ผู้ใช้_เครือข่าย import เครื่องเสมือน

ตําแหน่ง = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('สื่อข้อมูล_เครื่องมือ', ตําแหน่ง / 'เครื่องมือ/เปิด_ที่เก็บ_สื่อข้อมูล.py')
สื่อข้อมูล_เครื่องมือ = importlib.util.module_from_spec(명세)
명세.loader.exec_module(สื่อข้อมูล_เครื่องมือ)

def แก้ไข_ค่า(เครื่อง, เนื้อหา_ค่า):
    เรียกใช้งาน = len(เครื่อง.บันทึก_สถิติ)
    เครื่อง.직렬.sendall(('edit note.txt\n' + เนื้อหา_ค่า + '\n.save\n').encode())
    return เครื่อง.ภาวะรอ('jkoros> ', เรียกใช้งาน)

def ดําเนินการ_คําสั่ง():
    ผลลัพธ์ = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        สื่อข้อมูล_ค่า = Path(임시) / 'files.img'
        สื่อข้อมูล_เครื่องมือ.เปิด_รายการ(สื่อข้อมูล_ค่า)
        เครื่อง = เครื่องเสมือน(ตําแหน่ง / 'build/kernel.elf', ที่เก็บ_กลาง=สื่อข้อมูล_ค่า)
        try:
            เครื่อง.คําสั่ง('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            แก้ไข_ค่า(เครื่อง, 'generation-one')
            เครื่อง.คําสั่ง('sync', ['Sync: 0'])
            แก้ไข_ค่า(เครื่อง, 'generation-two')
            เครื่อง.คําสั่ง('sync', ['Sync: 0'])
            แก้ไข_ค่า(เครื่อง, 'unsynced-three')
            ผลลัพธ์['save'] = เครื่อง.บันทึก_สถิติ.decode('utf-8', 'replace')
        finally:
            เครื่อง.ปิด()
        เครื่อง = เครื่องเสมือน(ตําแหน่ง / 'build/kernel.iso', 'iso', ที่เก็บ_กลาง=สื่อข้อมูล_ค่า)
        try:
            ข้อความออก = เครื่อง.คําสั่ง('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in ข้อความออก
            เครื่อง.คําสั่ง('cat stored.txt', ['saved-from-C'])
            ผลลัพธ์['restore'] = เครื่อง.บันทึก_สถิติ.decode('utf-8', 'replace')
        finally:
            เครื่อง.ปิด()
        ข้อมูล = bytearray(สื่อข้อมูล_ค่า.read_bytes())
        세대들 = [struct.unpack_from('<I', ข้อมูล, (1 + ดัชนี * 259) * 512 + 4)[0] for ดัชนี in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ข้อมูล[(1 + 최신 * 259 + 3) * 512] ^= 1
        สื่อข้อมูล_ค่า.write_bytes(ข้อมูล)
        เครื่อง = เครื่องเสมือน(ตําแหน่ง / 'build/kernel.elf', ที่เก็บ_กลาง=สื่อข้อมูล_ค่า)
        try:
            เครื่อง.คําสั่ง('cat note.txt', ['generation-one'])
            เครื่อง.คําสั่ง('cat stored.txt', ['saved-from-C'])
            ผลลัพธ์['checksum_fallback'] = เครื่อง.บันทึก_สถิติ.decode('utf-8', 'replace')
        finally:
            เครื่อง.ปิด()
        อัทเธอร์_สื่อข้อมูล = Path(임시) / 'foreign.img'
        อัทเธอร์_สื่อข้อมูล.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(อัทเธอร์_สื่อข้อมูล.read_bytes()).hexdigest()
        เครื่อง = เครื่องเสมือน(ตําแหน่ง / 'build/kernel.elf', ที่เก็บ_กลาง=อัทเธอร์_สื่อข้อมูล)
        try:
            เครื่อง.คําสั่ง('sync', ['Sync: -19'])
        finally:
            เครื่อง.ปิด()
        assert hashlib.sha256(อัทเธอร์_สื่อข้อมูล.read_bytes()).hexdigest() == 이전
        ผลลัพธ์['foreign_disk_unchanged'] = True
    (ตําแหน่ง / 'build/보존시험.json').write_text(json.dumps(ผลลัพธ์, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE เก็บ_ค่า/ISO 재부팅/검사합 กู้คืน_สถานะ/다른 สื่อข้อมูล_ค่า 비변경', flush=True)

if __name__ == '__main__':
    ดําเนินการ_คําสั่ง()
