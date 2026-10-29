#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/파일전송시험.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    การแมป_ค่า = {'timeout': '시간제한', 'payload': 'ส่วนข้อมูล_ข้อมูล', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ข้อมูล', 'proc': 'โพรเซส', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'เก็บถาวร', 'main': 'เรียกใช้งาน', 'net_source': 'สุทธิ_แหล่ง', 'temporary': '임시자원', 'static_source': 'คงที่_แหล่ง', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'แสดง_ราก', 'text': 'ข้อความ', 'marker': 'มาร์กเกอร์', 'EchoFixture': '되돌림시험서버', 'command': 'คําสั่ง', 'out': 'เมตริก_ข้อมูล', 'expected': '예상결과', 'server_source': 'เซิร์ฟเวอร์_แหล่ง', 'shell': 'เชลล์', 'upload': 'อัปโหลด_ไฟล์', 'transcript': 'การถอดความ', 'port': 'หมายเลขพอร์ต', 'native': 'ดั้งเดิม', 'elf': 'แฟ้มปฏิบัติการ', 'server_udp_port': 'เซิร์ฟเวอร์_เดตาแกรม_แปลง', 'packed': '묶인자료', 'bridge': 'บริดจ์', 'selector': 'ตัวเลือก_582fe3b9', 'end': 'สิ้นสุดการโทร_ออฟเซต', 'e': '보조항목', 'ftp': 'การถ่ายโอนแฟ้ม_เพื่อน', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'ชั้น_ค่า', 'result': 'ผลลัพธ์', 'unchanged': '보존자료', 'line': 'บรรทัด', 'server_tcp_port': 'เซิร์ฟเวอร์_สตรีม_แปลง', 'source': '원본자료', 'NetworkBridge': 'บริดจ์_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'รับ_อีเมล', 'report': 'การตรวจสอบความถูกต้อง_รายงาน'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
