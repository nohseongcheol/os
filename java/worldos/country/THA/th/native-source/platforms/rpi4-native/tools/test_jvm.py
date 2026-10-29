#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/자바가상기계시험.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    การแมป_ค่า = {'message': 'ข้อสังเกต_ข้อความ', 's': 'สตริง_ข้อมูล', 'actual': 'ค่าจริง_เมตริก', 'match': '일치', 'payload': 'ส่วนข้อมูล_ข้อมูล', 'cases': 'กรณีทดสอบ', 'fixture': 'การทดสอบ_ข้อมูล', 'main': 'เรียกใช้งาน', 'ROOT': 'แสดง_ราก', 'text': 'ข้อความ', 'valid': 'ถูกต้อง', 'includes': '포함인수', 'include': 'รวม_e6c90571', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'เสร็จสมบูรณ์_จํานวน', 'classes': 'คลาส_พาธ', 'output': 'ผลผลิต', 'result': 'ผลลัพธ์', 'cmd': '명령인수', 'name': 'ชื่อ', 'jar': '자바꾸러미', 'report': 'การตรวจสอบความถูกต้อง_รายงาน', 'tests': 'รายการทดสอบ'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
