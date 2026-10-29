#!/usr/bin/env python3
"""한국어 네트워크 예제용 вузел TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,пратакол_кіравання_перадачай_TCP_порт=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);дадзеныя=bytearray()
                while b'\n' not in дадзеныя and len(дадзеныя)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    дадзеныя.extend(조각)
                수신됨.append(('tcp',bytes(дадзеныя)));자신.request.sendall(дадзеныя)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                дадзеныя,소켓=자신.request;수신됨.append(('udp',дадзеныя));소켓.sendto(дадзеныя,자신.client_address)
        자신.кантакт_кіраванне=socketserver.ThreadingTCPServer(('127.0.0.1',пратакол_кіравання_перадачай_TCP_порт),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.кантакт_кіраванне.server_close();raise
        자신.кантакт_кіраванне.daemon_threads=자신.전문제어.daemon_threads=True
        자신.пратакол_кіравання_перадачай_TCP_порт=자신.кантакт_кіраванне.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for сервер_значэнне in (자신.кантакт_кіраванне,자신.전문제어):
            작업가닥=threading.Thread(target=сервер_значэнне.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*аргумент_масіў):
        for сервер_значэнне in (자신.кантакт_кіраванне,자신.전문제어):сервер_значэнне.shutdown();сервер_значэнне.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    аналізатар=argparse.ArgumentParser(description=__doc__)
    аналізатар.add_argument('--tcp-port',type=int,default=9000);аналізатар.add_argument('--udp-port',type=int,default=9001)
    аргумент_масіў=аналізатар.parse_args()
    with 되돌림서버(аргумент_масіў.tcp_port,аргумент_масіў.udp_port) as 되돌림서버항목:
        print('вузел TCP {}, UDP {} Падрыхтаваць. 게스트 адрас: 10.0.2.2. Выхад_праграма: Ctrl+C'.format(되돌림서버항목.пратакол_кіравання_перадачай_TCP_порт,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
