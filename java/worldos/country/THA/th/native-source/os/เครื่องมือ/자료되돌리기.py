#!/usr/bin/env python3
"""โฮสต์ 루프백 주소에만 바인딩하는 UDP 시험 เซิร์ฟเวอร์_ค่า. Ctrl+C로 종료한다."""
import argparse
import socket

def ดําเนินการ_คําสั่ง():
    แยกวิเคราะห์_ค่า = argparse.ArgumentParser(description='jkoros ผู้ใช้ UDP 예제의 로컬 ส่งคืน_บริดจ์ เซิร์ฟเวอร์_ค่า')
    แยกวิเคราะห์_ค่า.add_argument('--port', type=int, default=9000)
    พารามิเตอร์_อาร์กิวเมนต์ = แยกวิเคราะห์_ค่า.parse_args()
    if not 1 <= พารามิเตอร์_อาร์กิวเมนต์.port <= 65535: แยกวิเคราะห์_ค่า.error('แปลง_ค่า 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as เซิร์ฟเวอร์_ค่า:
        เซิร์ฟเวอร์_ค่า.bind(('127.0.0.1', พารามิเตอร์_อาร์กิวเมนต์.port))
        print('UDP 127.0.0.1:{} จัดเตรียม. Ctrl+C로 ออก_แอป.'.format(พารามิเตอร์_อาร์กิวเมนต์.port), flush=True)
        while True:
            ข้อมูล, ชั้น_ค่า = เซิร์ฟเวอร์_ค่า.recvfrom(65535)
            เซิร์ฟเวอร์_ค่า.sendto(ข้อมูล, ชั้น_ค่า)

if __name__ == '__main__':
    try: ดําเนินการ_คําสั่ง()
    except KeyboardInterrupt: pass
