#!/usr/bin/env python3
"""한국어 네트워크 예제용 хост_рачунар TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,TCP_порт=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);подаци=bytearray()
                while b'\n' not in подаци and len(подаци)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    подаци.extend(조각)
                수신됨.append(('tcp',bytes(подаци)));자신.request.sendall(подаци)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                подаци,소켓=자신.request;수신됨.append(('udp',подаци));소켓.sendto(подаци,자신.client_address)
        자신.веза_контрола=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_порт),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.веза_контрола.server_close();raise
        자신.веза_контрола.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_порт=자신.веза_контрола.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for сервер_вриједност in (자신.веза_контрола,자신.전문제어):
            작업가닥=threading.Thread(target=сервер_вриједност.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*аргумент_низ):
        for сервер_вриједност in (자신.веза_контрола,자신.전문제어):сервер_вриједност.shutdown();сервер_вриједност.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    аргумент_низ=인수해석기.parse_args()
    with 되돌림서버(аргумент_низ.tcp_port,аргумент_низ.udp_port) as 되돌림서버항목:
        print('хост_рачунар TCP {}, UDP {} Припремити. 게스트 адреса: 10.0.2.2. изаћи_програм: Ctrl+C'.format(되돌림서버항목.TCP_порт,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
