#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/예제되돌림서버.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제되돌림서버')
    การแมป_ค่า = {'data': 'ข้อมูล', 'sock': '소켓', 'tcp_port': '연결접속번호', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': 'เดตาแกรม_จุดจับ_คําขอ', 'thread': 'งานเบื้องหลัง', 'echo': '되돌림서버항목', 'TCP': 'จุดจับ_เพื่อน_คําขอ', 'EchoServers': '되돌림서버', 'parser': 'ตัวแยกวิเคราะห์', 'server': 'เซิร์ฟเวอร์_ค่า', 'udp_port': '전문접속번호', 'args': 'อาร์กิวเมนต์_อาร์เรย์'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
