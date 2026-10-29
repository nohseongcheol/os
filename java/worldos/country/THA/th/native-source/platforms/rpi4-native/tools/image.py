#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/เปิด_รูป.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('เปิด_รูป', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('เปิด_รูป')
    การแมป_ค่า = {'total': 'รวม_ความจุ', 'start': 'เรียกใช้งาน', 'firmware': 'เฟิร์มแวร์_ค่า', 'files': 'แฟ้ม_รายการ', 'archive_base': 'เก็บถาวร_ฐาน', 'partition': 'พาร์ติชัน_แฟ้ม', 'archive': 'เก็บถาวร', 'main': 'เรียกใช้งาน', 'block': 'ข้อมูล_บล็อก', 'ROOT': 'แสดง_ราก', 'boot': '부팅경로', 'stage': 'สเตจ_ค่า', 'out': 'เมตริก_ข้อมูล', 'expected': '예상결과', 'f': 'แฟ้ม_รายการ_3d0c1245', 'src': '원본주소', 'path': 'เส้นทาง', 'p': 'ข้อมูล_ตําแหน่ง', 'extracted': '추출자료', 'member': 'สมาชิก', 'mbr': 'มาสเตอร์บูตเรกคอร์ด', 'image': 'รูป', 'sector_count': '섹터개수', 'dist': 'การกระจาย_พาธ', 'sha': '해시계산', 'license_': 'สิทธิการใช้งาน', 'source': '원본자료', 'name': 'ชื่อ', 'value': 'ค่า', 'manifest': 'รวม_ไฟล์กํากับ', 'dest': 'ปลายทาง_ค่า_ตําแหน่ง', 'work': '작업경로'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
