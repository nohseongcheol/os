#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/개발꾸러미번역.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('개발꾸러미번역', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('개발꾸러미번역')
    การแมป_ค่า = {'compiler': 'คอมไพเลอร์_เครื่องมือ', 'obj': 'แฟ้มปลายทาง', 'sdk': 'ชุดเครื่องมือการพัฒนา', 'output': 'ผลผลิต', 'main': 'เรียกใช้งาน', 'elf': 'แฟ้มปฏิบัติการ', 'is_c': '시언어여부', 'parser': 'ตัวแยกวิเคราะห์', 'language': 'ภาษา', 'work': '작업경로', 'args': 'อาร์กิวเมนต์_อาร์เรย์'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
