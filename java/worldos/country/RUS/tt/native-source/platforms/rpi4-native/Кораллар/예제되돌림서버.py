#!/usr/bin/env python3
"""Татарча 네트워크 예제용 хост TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,TCP_протоколы_порт=0,UDP_порт=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);мәгълүмат=bytearray()
                while b'\n' not in мәгълүмат and len(мәгълүмат)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    мәгълүмат.extend(조각)
                수신됨.append(('tcp',bytes(мәгълүмат)));자신.request.sendall(мәгълүмат)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                мәгълүмат,소켓=자신.request;수신됨.append(('udp',мәгълүмат));소켓.sendto(мәгълүмат,자신.client_address)
        자신.тоташу_идарә=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_протоколы_порт),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_порт),전문요청처리)
        except Exception:자신.тоташу_идарә.server_close();raise
        자신.тоташу_идарә.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_протоколы_порт=자신.тоташу_идарә.server_address[1];자신.UDP_порт=자신.전문제어.server_address[1]

    def __enter__(자신):
        for сервер_VALUE in (자신.тоташу_идарә,자신.전문제어):
            작업가닥=threading.Thread(target=сервер_VALUE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*аргумент_МАССИВ):
        for сервер_VALUE in (자신.тоташу_идарә,자신.전문제어):сервер_VALUE.shutdown();сервер_VALUE.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    аргумент_МАССИВ=인수해석기.parse_args()
    with 되돌림서버(аргумент_МАССИВ.tcp_port,аргумент_МАССИВ.udp_port) as 되돌림서버항목:
        print('хост TCP {}, UDP {} Әзерләү. 게스트 адрес: 10.0.2.2. Чыгу_кушымта: Ctrl+C'.format(되돌림서버항목.TCP_протоколы_порт,되돌림서버항목.UDP_порт),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
