#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/อัปโหลด_ไฟล์.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('อัปโหลด_ไฟล์', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('อัปโหลด_ไฟล์')
    การแมป_ค่า = {'data': 'ข้อมูล', 'i': '순번', 'name': 'ชื่อ', 'c': 'รหัสอักขระ', 'p': 'ข้อมูล_ตําแหน่ง', 'args': 'อาร์กิวเมนต์_อาร์เรย์'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
