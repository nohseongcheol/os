#!/usr/bin/env python3
"""Македонски 네트워크 예제용 вдоми TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,ТЦП_порта=0,УДП_порта=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class рачка_врска_Барање_на_HTTP(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);податоци=bytearray()
                while b'\n' not in податоци and len(податоци)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    податоци.extend(조각)
                수신됨.append(('tcp',bytes(податоци)));자신.request.sendall(податоци)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                податоци,소켓=자신.request;수신됨.append(('udp',податоци));소켓.sendto(податоци,자신.client_address)
        자신.врска_контрола=socketserver.ThreadingTCPServer(('127.0.0.1',ТЦП_порта),рачка_врска_Барање_на_HTTP)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',УДП_порта),전문요청처리)
        except Exception:자신.врска_контрола.server_close();raise
        자신.врска_контрола.daemon_threads=자신.전문제어.daemon_threads=True
        자신.ТЦП_порта=자신.врска_контрола.server_address[1];자신.УДП_порта=자신.전문제어.server_address[1]

    def __enter__(자신):
        for сервер_VALUE in (자신.врска_контрола,자신.전문제어):
            작업가닥=threading.Thread(target=сервер_VALUE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*аргумент_низа):
        for сервер_VALUE in (자신.врска_контрола,자신.전문제어):сервер_VALUE.shutdown();сервер_VALUE.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    анализатор=argparse.ArgumentParser(description=__doc__)
    анализатор.add_argument('--tcp-port',type=int,default=9000);анализатор.add_argument('--udp-port',type=int,default=9001)
    аргумент_низа=анализатор.parse_args()
    with 되돌림서버(аргумент_низа.tcp_port,аргумент_низа.udp_port) as 되돌림서버항목:
        print('вдоми TCP {}, UDP {} Подготви. 게스트 адреса: 10.0.2.2. Излез_програма: Ctrl+C'.format(되돌림서버항목.ТЦП_порта,되돌림서버항목.УДП_порта),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
