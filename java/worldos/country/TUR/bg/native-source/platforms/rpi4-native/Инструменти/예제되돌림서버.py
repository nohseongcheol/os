#!/usr/bin/env python3
"""Български 네트워크 예제용 хост TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class Ехо_Сървъри:
    def __init__(자신,연결접속번호=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class манипулатор_връзка_искане(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);данни=bytearray()
                while b'\n' not in данни and len(данни)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    данни.extend(조각)
                수신됨.append(('tcp',bytes(данни)));자신.request.sendall(данни)
        class дейтаграма_манипулатор_искане(socketserver.BaseRequestHandler):
            def handle(자신):
                данни,소켓=자신.request;수신됨.append(('udp',данни));소켓.sendto(данни,자신.client_address)
        자신.връзка_контрол=socketserver.ThreadingTCPServer(('127.0.0.1',연결접속번호),манипулатор_връзка_искане)
        try:자신.дейтаграма_контрол=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),дейтаграма_манипулатор_искане)
        except Exception:자신.връзка_контрол.server_close();raise
        자신.връзка_контрол.daemon_threads=자신.дейтаграма_контрол.daemon_threads=True
        자신.연결접속번호=자신.връзка_контрол.server_address[1];자신.전문접속번호=자신.дейтаграма_контрол.server_address[1]

    def __enter__(자신):
        for сървър_стойност in (자신.връзка_контрол,자신.дейтаграма_контрол):
            작업가닥=threading.Thread(target=сървър_стойност.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*аргумент_масив):
        for сървър_стойност in (자신.връзка_контрол,자신.дейтаграма_контрол):сървър_стойност.shutdown();сървър_стойност.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    анализатор=argparse.ArgumentParser(description=__doc__)
    анализатор.add_argument('--tcp-port',type=int,default=9000);анализатор.add_argument('--udp-port',type=int,default=9001)
    аргумент_масив=анализатор.parse_args()
    with Ехо_Сървъри(аргумент_масив.tcp_port,аргумент_масив.udp_port) as Ехо_сървър_запис:
        print('хост TCP {}, UDP {} Подготвяне. 게스트 адрес: 10.0.2.2. Изход_програма: Ctrl+C'.format(Ехо_сървър_запис.연결접속번호,Ехо_сървър_запис.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
