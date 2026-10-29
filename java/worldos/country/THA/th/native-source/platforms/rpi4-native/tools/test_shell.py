#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/การทดสอบ_เชลล์.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('การทดสอบ_เชลล์', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('การทดสอบ_เชลล์')
    การแมป_ค่า = {'timeout': '시간제한', 'x': 'พิกัดแกน_x', 'msg': 'เครือข่าย_อีเมล', 'i': '순번', 'reply': 'ตอบกลับ', 'call': '호출', 'args': 'อาร์กิวเมนต์_อาร์เรย์', 'chunk': '조각', 'data': 'ข้อมูล', 'proc': 'โพรเซส', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ส่ง', 'file': 'แฟ้ม', 'main': 'เรียกใช้งาน', 'found': 'ค้นหา_เมตริก', 'ROOT': 'แสดง_ราก', 'text': 'ข้อความ', 'marker': 'มาร์กเกอร์', 'command': 'คําสั่ง', 'expected': '예상결과', 'pixel': 'พิกเซล', 'shell': 'เชลล์', 'poll': '준비살피미', 'transcript': 'การถอดความ', 'end': 'สิ้นสุดการโทร_ออฟเซต', 'image': 'รูป', 'key': '누름값', 'y': '세로좌표', 'output': 'ผลผลิต', 'result': 'ผลลัพธ์', 'client': 'ไคลเอ็นต์', 'line': 'บรรทัด', 'stream': 'สตรีม_ค่า', 'name': 'ชื่อ', 'value': 'ค่า', 'receive': 'รับ_อีเมล', 'report': 'การตรวจสอบความถูกต้อง_รายงาน', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
