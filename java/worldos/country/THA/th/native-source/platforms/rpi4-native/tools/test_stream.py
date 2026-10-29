#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/การทดสอบ_สตรีม.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('การทดสอบ_สตรีม', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('การทดสอบ_สตรีม')
    การแมป_ค่า = {'out': 'เมตริก_ข้อมูล', 'main': 'เรียกใช้งาน', 'ROOT': 'แสดง_ราก', 'p': 'ข้อมูล_ตําแหน่ง', 'text': 'ข้อความ', 'report': 'การตรวจสอบความถูกต้อง_รายงาน'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
