#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/เดสก์ท็อป_ดู.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('เดสก์ท็อป_ดู', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('เดสก์ท็อป_ดู')
    การแมป_ค่า = {'count': '항목수', 'special': '특수글쇠', 'error': 'ข้อผิดพลาด', 'exact': '정확한값', 'network': 'เครือข่าย_9b2e3222', 'closed': 'เทคโนโลยีสารสนเทศ_ปิด', 'length': '길이', 'opened': '열림', 'ftp_port': 'การถ่ายโอนแฟ้ม_หมายเลขพอร์ต', 'server': 'เซิร์ฟเวอร์_ค่า', 'resources': 'แหล่งข้อมูล', 'data': 'ข้อมูล', 'shift': 'เลื่อน_คีย์', 'send': 'ส่ง', 'run_desktop': 'ใช้งาน_เดสก์ท็อป', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'โฮสต์', 'text': 'ข้อความ', 'korean': '한글여부', 'port': 'หมายเลขพอร์ต', 'signum': 'สัญญาณ_หมายเลข', 'version': 'หมายเลขรุ่น', 'parser': 'ตัวแยกวิเคราะห์', 'bridge': 'บริดจ์', 'kind': 'ประเภท_ค่า', 'tail': '끝부분', 'size': 'ขนาด', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'ไคลเอ็นต์', 'char': 'ข้อมูลอักขระ', 'work': '작업경로', 'Keyboard': 'คีย์บอร์ด', 'x': 'พิกัดแกน_x', 'down': '누르는중', 'net': 'บริดจ์_รายการ', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'อาร์กิวเมนต์_อาร์เรย์', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'โพรเซส', 'Desktop': 'เชื่อมต่อ_เดสก์ท็อป', 'buttons': '단추들', 'thread': 'งานเบื้องหลัง', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'สลับ_โหมด', 'command': 'คําสั่ง', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'ควบคุม_คีย์', 'path': 'เส้นทาง', 'cp': 'อักขระ_การเข้ารหัส', 'terminate': 'สิ้นสุด', 'security': 'ความปลอดภัย', 'vnc_port': '원격화면접속번호', 'body': 'เนื้อความ', 'index': 'การค้นหา_ดัชนี', 'exited': '종료됨', 'keysym': 'คีย์_สัญลักษณ์', 'output': 'ผลผลิต', 'keyboard': 'คีย์บอร์ด_รายการ', 'interrupted': '가로채기됨', 'listener': 'รับ_แปลง', 'reader': 'ผู้อ่าน', 'NetworkBridge': 'บริดจ์_3de4fe3a', 'gui': '그림화면', 'worker': 'การประมวลผล_งาน'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
