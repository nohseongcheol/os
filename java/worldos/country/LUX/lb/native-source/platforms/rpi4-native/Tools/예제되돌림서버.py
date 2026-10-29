#!/usr/bin/env python3
"""한국어 네트워크 예제용 Host TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,TCP_Port=0,UDP_Port=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);Daten=bytearray()
                while b'\n' not in Daten and len(Daten)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    Daten.extend(조각)
                수신됨.append(('tcp',bytes(Daten)));자신.request.sendall(Daten)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                Daten,소켓=자신.request;수신됨.append(('udp',Daten));소켓.sendto(Daten,자신.client_address)
        자신.Verbindung_Kontroll=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_Port),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_Port),전문요청처리)
        except Exception:자신.Verbindung_Kontroll.server_close();raise
        자신.Verbindung_Kontroll.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_Port=자신.Verbindung_Kontroll.server_address[1];자신.UDP_Port=자신.전문제어.server_address[1]

    def __enter__(자신):
        for Server_VALUE in (자신.Verbindung_Kontroll,자신.전문제어):
            작업가닥=threading.Thread(target=Server_VALUE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*Argument_ARRAY):
        for Server_VALUE in (자신.Verbindung_Kontroll,자신.전문제어):Server_VALUE.shutdown();Server_VALUE.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    Argument_ARRAY=인수해석기.parse_args()
    with 되돌림서버(Argument_ARRAY.tcp_port,Argument_ARRAY.udp_port) as 되돌림서버항목:
        print('Host TCP {}, UDP {} Préparéieren. 게스트 Adress: 10.0.2.2. Schluss_App: Ctrl+C'.format(되돌림서버항목.TCP_Port,되돌림서버항목.UDP_Port),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
