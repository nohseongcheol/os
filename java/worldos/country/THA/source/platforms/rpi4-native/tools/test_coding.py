#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/코딩시험.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('코딩시험')
    การแมป_ค่า = {'out': 'เมตริก_ข้อมูล', 'expected': '예상결과', 'sdk': 'ชุดเครื่องมือการพัฒนา', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'เรียกใช้งาน', 'elf': 'แฟ้มปฏิบัติการ', 'run': 'ดําเนินการ_คําสั่ง', 'name': 'ชื่อ', 'path': 'เส้นทาง', 'p': 'ข้อมูล_ตําแหน่ง', 'ROOT': 'แสดง_ราก', 'report': 'การตรวจสอบความถูกต้อง_รายงาน', 'args': 'อาร์กิวเมนต์_อาร์เรย์'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
