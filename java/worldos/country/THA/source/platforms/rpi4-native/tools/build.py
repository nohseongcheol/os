#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/สร้าง.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('สร้าง', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('สร้าง')
    การแมป_ค่า = {'network': 'เครือข่าย_9b2e3222', 'BUILD': 'รุ่น_พาธ', 'ar': 'เก็บถาวร_เครื่องมือ', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ฟอนต์_ข้อมูล', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'อาร์กิวเมนต์_อาร์เรย์', 'source_flags': '원본설정', 'ld': 'ตัวเชื่อมโยง_เครื่องมือ', 'method': 'เมธอด_รายการ', 'main': 'เรียกใช้งาน', 'objcopy': 'วัตถุ_แฟ้ม_ตัวแปลง', 'ROOT': 'แสดง_ราก', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'คอมไพเลอร์_เครื่องมือ', 'build_users': 'เปิด_ผู้ใช้_สเปซ', 'f': 'แฟ้ม_รายการ_3d0c1245', 'extra': '추가영역', 'exports': 'ส่งออก_ตาราง', 'jobs': '빌드작업', 'run': 'ดําเนินการ_คําสั่ง', 'path': 'เส้นทาง', 'REPO': 'ที่เก็บ_ราก', 'tool': 'เครื่องมือ', 'classes': 'คลาส_พาธ', 'output': 'ผลผลิต', 'samples': '예제들', 'symbol': 'สัญลักษณ์_ค่า', 'source': '원본자료', 'name': 'ชื่อ', 'build_network': 'เปิด_เครือข่าย_48d29d6d', 'font_info': 'ฟอนต์_ข้อมูล_c16c0f1c', 'manifest': 'รวม_ไฟล์กํากับ', 'work': '작업경로'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
