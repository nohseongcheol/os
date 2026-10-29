#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/예제빌드.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    การแมป_ค่า = {'out': 'เมตริก_ข้อมูล', 'build_examples': '예제만들기', 'files': 'แฟ้ม_รายการ', 'java': '자바실행', 'run': 'ดําเนินการ_คําสั่ง', 'path': 'เส้นทาง', 'p': 'ข้อมูล_ตําแหน่ง', 'readme': '안내자료', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'การค้นหา_ดัชนี', 'classes': 'คลาส_พาธ', 'repo': 'ที่เก็บ_พาธ', 'root': 'ราก_อีเมล', 'content': 'เนื้อหา_ค่า', 'source': '원본자료', 'name': 'ชื่อ', 'target': 'เป้าหมาย', 'manifest': 'รวม_ไฟล์กํากับ', 'language': 'ภาษา'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
