#!/usr/bin/env python3
"""ไทย 네트워크 예제용 โฮสต์ TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,연결접속번호=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class จุดจับ_เพื่อน_คําขอ(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);ข้อมูล=bytearray()
                while b'\n' not in ข้อมูล and len(ข้อมูล)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    ข้อมูล.extend(조각)
                수신됨.append(('tcp',bytes(ข้อมูล)));자신.request.sendall(ข้อมูล)
        class เดตาแกรม_จุดจับ_คําขอ(socketserver.BaseRequestHandler):
            def handle(자신):
                ข้อมูล,소켓=자신.request;수신됨.append(('udp',ข้อมูล));소켓.sendto(ข้อมูล,자신.client_address)
        자신.เพื่อน_ควบคุม=socketserver.ThreadingTCPServer(('127.0.0.1',연결접속번호),จุดจับ_เพื่อน_คําขอ)
        try:자신.เดตาแกรม_ควบคุม=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),เดตาแกรม_จุดจับ_คําขอ)
        except Exception:자신.เพื่อน_ควบคุม.server_close();raise
        자신.เพื่อน_ควบคุม.daemon_threads=자신.เดตาแกรม_ควบคุม.daemon_threads=True
        자신.연결접속번호=자신.เพื่อน_ควบคุม.server_address[1];자신.전문접속번호=자신.เดตาแกรม_ควบคุม.server_address[1]

    def __enter__(자신):
        for เซิร์ฟเวอร์_ค่า in (자신.เพื่อน_ควบคุม,자신.เดตาแกรม_ควบคุม):
            งานเบื้องหลัง=threading.Thread(target=เซิร์ฟเวอร์_ค่า.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            งานเบื้องหลัง.start();자신.작업가닥들.append(งานเบื้องหลัง)
        return 자신

    def __exit__(자신,*อาร์กิวเมนต์_อาร์เรย์):
        for เซิร์ฟเวอร์_ค่า in (자신.เพื่อน_ควบคุม,자신.เดตาแกรม_ควบคุม):เซิร์ฟเวอร์_ค่า.shutdown();เซิร์ฟเวอร์_ค่า.server_close()
        for งานเบื้องหลัง in 자신.작업가닥들:งานเบื้องหลัง.join(timeout=1)


if __name__=='__main__':
    ตัวแยกวิเคราะห์=argparse.ArgumentParser(description=__doc__)
    ตัวแยกวิเคราะห์.add_argument('--tcp-port',type=int,default=9000);ตัวแยกวิเคราะห์.add_argument('--udp-port',type=int,default=9001)
    อาร์กิวเมนต์_อาร์เรย์=ตัวแยกวิเคราะห์.parse_args()
    with 되돌림서버(อาร์กิวเมนต์_อาร์เรย์.tcp_port,อาร์กิวเมนต์_อาร์เรย์.udp_port) as 되돌림서버항목:
        print('โฮสต์ TCP {}, UDP {} จัดเตรียม. 게스트 อีเมล: 10.0.2.2. ออก_แอป: Ctrl+C'.format(되돌림서버항목.연결접속번호,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
