#!/usr/bin/env python3
"""기존 เส้นทาง 호환 จุดเข้าใช้งาน. ค่าจริง_ข้อมูล 구현: ../เครื่องมือ/บริดจ์_3de4fe3a.py"""
import importlib as 가져오기
import sys as ระบบปฏิบัติการ_ค่า
from pathlib import Path as เส้นทาง
ระบบปฏิบัติการ_ค่า.path.insert(0, str(เส้นทาง(__file__).resolve().parents[1] / 'เครื่องมือ'))
if __name__ == '__main__':
    import runpy as แอป_ลิ้นชักแอป
    แอป_ลิ้นชักแอป.run_module('บริดจ์_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('บริดจ์_3de4fe3a')
    การแมป_ค่า = {'response': 'การตอบ', 'parts': 'พาธ_คอมโพเนนต์', 's': 'สตริง_ข้อมูล', 'i': '순번', 'close': 'ปิด', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'รายการ_ค่า', 'flags': '설정비트', 'ftp_port': 'การถ่ายโอนแฟ้ม_หมายเลขพอร์ต', 'args': 'อาร์กิวเมนต์_อาร์เรย์', 'server': 'เซิร์ฟเวอร์_ค่า', 'data': 'ข้อมูล', 'ethernet_input': '이더넷입력', 'trace_packet': 'เทรซ_แพคเก็ต', 'GATEWAY': 'เกตเวย์_ฮาร์ดแวร์_อีเมล', 'rule': 'กฎ_ค่า', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'โฮสต์', 'ack': '확인번호', 'serial_port': 'พอร์ต_COM_หมายเลข', 'readers': '읽기대상들', 'guest': 'ผู้เยี่ยมชม', 'destination': 'ปลายทาง_ข้อมูล_อีเมล', 'ethernet_port': 'พอร์ตอีเทอร์เน็ต', 'b': '둘째값', 'MAC': 'เลขที่อยู่จริง', 'arp': 'อีเมล_ความละเอียด_แพคเก็ต', 'writable': '쓸수있음', 'direction': '방향', 'seq': 'ลําดับ_หมายเลข', 'frame': '실행틀', 'loop': 'วงกลม_ค่า', 'port': 'หมายเลขพอร์ต', 'offset': 'ออฟเซต_ค่า', 'readable': '읽을수있음', 'c': 'รหัสอักขระ', 'p': 'ข้อมูล_ตําแหน่ง', 'writers': '쓰기대상들', 'IP': 'ที่อยู่อินเทอร์เน็ต_ค่า', 'e': '보조항목', 'n': '개수', 'packet': 'แพคเก็ต_ข้อมูล', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'บริดจ์_3de4fe3a', 'window': 'หน้าต่าง', 'capture': 'จับ'}
    for 이전, ปัจจุบัน_รายการ in การแมป_ค่า.items():
        if hasattr(구현, ปัจจุบัน_รายการ): globals()[이전] = getattr(구현, ปัจจุบัน_รายการ)
