#!/usr/bin/env python3
"""한국어 네트워크 예제용 hou TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,TCP_ombou=0,GDP_Gebruikersdatagramprotokol_ombou=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);data=bytearray()
                while b'\n' not in data and len(data)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    data.extend(조각)
                수신됨.append(('tcp',bytes(data)));자신.request.sendall(data)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                data,소켓=자신.request;수신됨.append(('udp',data));소켓.sendto(data,자신.client_address)
        자신.verbinding_kontrole=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_ombou),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',GDP_Gebruikersdatagramprotokol_ombou),전문요청처리)
        except Exception:자신.verbinding_kontrole.server_close();raise
        자신.verbinding_kontrole.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_ombou=자신.verbinding_kontrole.server_address[1];자신.GDP_Gebruikersdatagramprotokol_ombou=자신.전문제어.server_address[1]

    def __enter__(자신):
        for bediener_VALUE in (자신.verbinding_kontrole,자신.전문제어):
            작업가닥=threading.Thread(target=bediener_VALUE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*argument_ARRAY):
        for bediener_VALUE in (자신.verbinding_kontrole,자신.전문제어):bediener_VALUE.shutdown();bediener_VALUE.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    ontleder=argparse.ArgumentParser(description=__doc__)
    ontleder.add_argument('--tcp-port',type=int,default=9000);ontleder.add_argument('--udp-port',type=int,default=9001)
    argument_ARRAY=ontleder.parse_args()
    with 되돌림서버(argument_ARRAY.tcp_port,argument_ARRAY.udp_port) as 되돌림서버항목:
        print('hou TCP {}, UDP {} Maak_gereed. 게스트 adres: 10.0.2.2. Verlaat_program: Ctrl+C'.format(되돌림서버항목.TCP_ombou,되돌림서버항목.GDP_Gebruikersdatagramprotokol_ombou),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
