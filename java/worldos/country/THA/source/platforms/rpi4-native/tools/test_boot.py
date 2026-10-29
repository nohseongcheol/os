#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/부팅시험.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    การแมป_ค่า = {'timeout': '시간제한', 'response': 'การตอบ', 'msg': 'เครือข่าย_อีเมล', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'เรียกทํางาน', 'cancel': 'ยกเลิก_ศัลยกรรม', 'cmd_byte': 'คําสั่ง_ไบต์', 'reply': 'ตอบกลับ', 'points': '지점들', 'server': 'เซิร์ฟเวอร์_ค่า', 'data': 'ข้อมูล', 'prompt': 'พร้อมท์', 'enter': 'ใส่', 'imported': '들여온파일', 'send': 'ส่ง', 'main': 'เรียกใช้งาน', 'ROOT': 'แสดง_ราก', 'text': 'ข้อความ', 'first_gui': '첫화면', 'pixel': 'พิกเซล', 'java_class': '자바클래스', 'upload': 'อัปโหลด_ไฟล์', 'pixels_file': 'พิกเซล_แฟ้ม', 'pixels_data': 'พิกเซล_ข้อมูล', 'edit': 'แก้ไข_ค่า', 'receive_until': '표시까지받기', 'selector': 'ตัวเลือก_582fe3b9', 'size': 'ขนาด', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'ผลลัพธ์', 'samples': '예제들', 'client': 'ไคลเอ็นต์', 'line': 'บรรทัด', 'report': 'การตรวจสอบความถูกต้อง_รายงาน', 'work': '작업경로', 'x': 'พิกัดแกน_x', 'python_checks': '파이썬검사', 'download': 'ดาวน์โหลด', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'วันครบกําหนด_เวลา', 'proc': 'โพรเซส', 'content': 'เนื้อหา_ค่า', 'block': 'ข้อมูล_บล็อก', 'marker': 'มาร์กเกอร์', 'command': 'คําสั่ง', 'expected': '예상결과', 'shell': 'เชลล์', 'drawing': 'รูปวาด_พาธ', 'f': 'แฟ้ม_รายการ_3d0c1245', 'transcript': 'การถอดความ', 'offset': 'ออฟเซต_ค่า', 'path': 'เส้นทาง', 'screenshot': 'สกรีนช็อต', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': 'ผลผลิต', 'stream': 'สตรีม_ค่า', 'cmd': '명령인수', 'name': 'ชื่อ', 'qmp': '모의제어접속'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
