#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    การแมป_ค่า = {'header': 'ส่วนหัว_ค่า', 'sources': '원문목록', 'i': '순번', 'info': 'ข้อมูลระบบ', 'payload': 'ส่วนข้อมูล_ข้อมูล', 'src': '원본주소', 'run': 'ดําเนินการ_คําสั่ง', 'build_java_library': '자바라이브러리만들기', 'relative': 'เส้นทางสัมพัทธ์', 'classes': 'คลาส_พาธ', 'dist': 'การกระจาย_พาธ', 'archive': 'เก็บถาวร', 'output': 'ผลผลิต', 'root': 'ราก_อีเมล', 'name': 'ชื่อ', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
