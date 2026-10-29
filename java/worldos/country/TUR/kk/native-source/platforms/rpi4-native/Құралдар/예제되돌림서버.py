#!/usr/bin/env python3
"""한국어 네트워크 예제용 орналастыру TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class экранға_шығару_Серверлер:
    def __init__(자신,TCP_протоколы_порт=0,пайдаланушы_датаграммасының_протоколы_порт=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);деректер=bytearray()
                while b'\n' not in деректер and len(деректер)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    деректер.extend(조각)
                수신됨.append(('tcp',bytes(деректер)));자신.request.sendall(деректер)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                деректер,소켓=자신.request;수신됨.append(('udp',деректер));소켓.sendto(деректер,자신.client_address)
        자신.қосылым_Басқару=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_протоколы_порт),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',пайдаланушы_датаграммасының_протоколы_порт),전문요청처리)
        except Exception:자신.қосылым_Басқару.server_close();raise
        자신.қосылым_Басқару.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_протоколы_порт=자신.қосылым_Басқару.server_address[1];자신.пайдаланушы_датаграммасының_протоколы_порт=자신.전문제어.server_address[1]

    def __enter__(자신):
        for сервер_мән in (자신.қосылым_Басқару,자신.전문제어):
            작업가닥=threading.Thread(target=сервер_мән.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*аргумент_массив):
        for сервер_мән in (자신.қосылым_Басқару,자신.전문제어):сервер_мән.shutdown();сервер_мән.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    талдау_құралы=argparse.ArgumentParser(description=__doc__)
    талдау_құралы.add_argument('--tcp-port',type=int,default=9000);талдау_құралы.add_argument('--udp-port',type=int,default=9001)
    аргумент_массив=талдау_құралы.parse_args()
    with экранға_шығару_Серверлер(аргумент_массив.tcp_port,аргумент_массив.udp_port) as экранға_шығару_сервер_енгізу:
        print('орналастыру TCP {}, UDP {} Дайындау. 게스트 мекенжай: 10.0.2.2. Шығу_бағдарлама: Ctrl+C'.format(экранға_шығару_сервер_енгізу.TCP_протоколы_порт,экранға_шығару_сервер_енгізу.пайдаланушы_датаграммасының_протоколы_порт),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
