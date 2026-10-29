#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/실행파일시험.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    การแมป_ค่า = {'out': 'เมตริก_ข้อมูล', 'expected': '예상결과', 'phoff': 'แอป_ส่วนหัว_ออฟเซต', 'offset': 'ออฟเซต_ค่า', 'invalid': 'ไม่ถูกต้อง_ข้อมูล', 'path': 'เส้นทาง', 'executable': 'แฟ้มปฏิบัติการ_รูป', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'ผลลัพธ์', 'format_': 'รูปแบบ_b87fd068', 'main': 'เรียกใช้งาน', 'content': 'เนื้อหา_ค่า', 'source': '원본자료', 'name': 'ชื่อ', 'reference': 'การเปรียบเทียบ_ขั้นต้น', 'ROOT': 'แสดง_ราก', 'value': 'ค่า', 'report': 'การตรวจสอบความถูกต้อง_รายงาน'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
