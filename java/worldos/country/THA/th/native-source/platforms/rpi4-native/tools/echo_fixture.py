#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/되돌림시험서버.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    การแมป_ค่า = {'data': 'ข้อมูล', 'e': '보조항목', 'connection': 'เพื่อน_e05f319b', 'f': 'แฟ้ม_รายการ_3d0c1245', 'peer': 'ชั้น_ค่า', 'self': '자신', 'udp': 'เดตาแกรม_ควบคุม', 't': 'เทอร์มินัล_รายการ', 'tcp': 'เพื่อน_ควบคุม', 'EchoFixture': '되돌림시험서버', 'args': 'อาร์กิวเมนต์_อาร์เรย์', 'chunk': '조각'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
