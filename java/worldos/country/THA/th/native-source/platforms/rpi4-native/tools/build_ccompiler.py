#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    การแมป_ค่า = {'out': 'เมตริก_ข้อมูล', 'builtins': '내장연산', 'header': 'ส่วนหัว_ค่า', 'sdk': 'ชุดเครื่องมือการพัฒนา', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': 'แฟ้มปฏิบัติการ', 'run': 'ดําเนินการ_คําสั่ง', 'flags': '설정비트', 'path': 'เส้นทาง', 'p': 'ข้อมูล_ตําแหน่ง', 'cc': '시언어번역기', 'obj': 'แฟ้มปลายทาง', 'flag': 'การตั้งค่า_ค่า', 'ld': 'ตัวเชื่อมโยง_เครื่องมือ', 'objects': 'ปลายทาง_ไฟล์', 'repo': 'ที่เก็บ_พาธ', 'v': '임시값', 'upstream': 'อัพสตรีม', 'root': 'ราก_อีเมล', 'assets': '탑재자료', 'source': '원본자료', 'name': 'ชื่อ', 'includes': '포함인수'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
