#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/파이썬빌드.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('파이썬빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파이썬빌드')
    การแมป_ค่า = {'ld': 'ตัวเชื่อมโยง_เครื่องมือ', 'archive': 'เก็บถาวร', 'SHA256': 'การตรวจสอบความถูกต้อง_แฮช', 'build_python': '파이썬만들기', 'root': 'ราก_อีเมล', 'source': '원본자료', 'name': 'ชื่อ', 'path': 'เส้นทาง', 'VERSION': 'รุ่น_ค่า_237a4c94', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'สมาชิก'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
