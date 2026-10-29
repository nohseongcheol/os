#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/ดําเนินการ_คําสั่ง.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('ดําเนินการ_คําสั่ง', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ดําเนินการ_คําสั่ง')
    การแมป_ค่า = {'supported': '지원목록', 'parser': 'ตัวแยกวิเคราะห์', 'qemu': '모의기계', 'run_desktop': 'ใช้งาน_เดสก์ท็อป', 'main': 'เรียกใช้งาน', 'host': 'โฮสต์', 'status': 'สถานะ_ค่า', 'NetworkBridge': 'บริดจ์_3de4fe3a', 'ROOT': 'แสดง_ราก', 'bridge': 'บริดจ์', 'loader': 'ตัวโหลด', 'base': 'พื้นหลัง_ค่า', 'options': 'ตัวเลือก', 'binary': 'ไบนารี', 'args': 'อาร์กิวเมนต์_อาร์เรย์', 'command': 'คําสั่ง'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
