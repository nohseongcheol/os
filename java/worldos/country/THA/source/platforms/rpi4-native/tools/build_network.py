#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/รุ่น_เครือข่าย.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('รุ่น_เครือข่าย', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('รุ่น_เครือข่าย')
    การแมป_ค่า = {'obj': 'แฟ้มปลายทาง', 'objects': 'ปลายทาง_ไฟล์', 'library': 'ไลบรารี', 'output': 'ผลผลิต', 'port': 'หมายเลขพอร์ต', 'root': 'ราก_อีเมล', 'files': 'แฟ้ม_รายการ', 'source': '원본자료', 'run': 'ดําเนินการ_คําสั่ง', 'flags': '설정비트', 'path': 'เส้นทาง', 'build_network': 'เปิด_เครือข่าย_48d29d6d', 'cc': '시언어번역기', 'ar': 'เก็บถาวร_เครื่องมือ'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
