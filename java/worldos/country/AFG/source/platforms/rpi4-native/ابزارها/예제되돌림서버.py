#!/usr/bin/env python3
"""فارسی 네트워크 예제용 میزبان TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,پروتکل_کنترل_مخابره_تبدیل=0,پروتکل_داده_نگار_کاربر_تبدیل=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);داده_ها=bytearray()
                while b'\n' not in داده_ها and len(داده_ها)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    داده_ها.extend(조각)
                수신됨.append(('tcp',bytes(داده_ها)));자신.request.sendall(داده_ها)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                داده_ها,소켓=자신.request;수신됨.append(('udp',داده_ها));소켓.sendto(داده_ها,자신.client_address)
        자신.اتصال_کنترل=socketserver.ThreadingTCPServer(('127.0.0.1',پروتکل_کنترل_مخابره_تبدیل),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',پروتکل_داده_نگار_کاربر_تبدیل),전문요청처리)
        except Exception:자신.اتصال_کنترل.server_close();raise
        자신.اتصال_کنترل.daemon_threads=자신.전문제어.daemon_threads=True
        자신.پروتکل_کنترل_مخابره_تبدیل=자신.اتصال_کنترل.server_address[1];자신.پروتکل_داده_نگار_کاربر_تبدیل=자신.전문제어.server_address[1]

    def __enter__(자신):
        for سرور_مقدار in (자신.اتصال_کنترل,자신.전문제어):
            작업가닥=threading.Thread(target=سرور_مقدار.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*آرگومان_آرايه):
        for سرور_مقدار in (자신.اتصال_کنترل,자신.전문제어):سرور_مقدار.shutdown();سرور_مقدار.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    مفسر=argparse.ArgumentParser(description=__doc__)
    مفسر.add_argument('--tcp-port',type=int,default=9000);مفسر.add_argument('--udp-port',type=int,default=9001)
    آرگومان_آرايه=مفسر.parse_args()
    with 되돌림서버(آرگومان_آرايه.tcp_port,آرگومان_آرايه.udp_port) as 되돌림서버항목:
        print('میزبان TCP {}, UDP {} آماده_کردن. 게스트 آدرس: 10.0.2.2. خروج_برنامه: Ctrl+C'.format(되돌림서버항목.پروتکل_کنترل_مخابره_تبدیل,되돌림서버항목.پروتکل_داده_نگار_کاربر_تبدیل),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
