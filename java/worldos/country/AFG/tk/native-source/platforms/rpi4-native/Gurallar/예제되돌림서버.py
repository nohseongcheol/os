#!/usr/bin/env python3
"""한국어 네트워크 예제용 esasy TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,TCP_port=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);maglumat=bytearray()
                while b'\n' not in maglumat and len(maglumat)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    maglumat.extend(조각)
                수신됨.append(('tcp',bytes(maglumat)));자신.request.sendall(maglumat)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                maglumat,소켓=자신.request;수신됨.append(('udp',maglumat));소켓.sendto(maglumat,자신.client_address)
        자신.birikme_dolandyryş=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_port),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.birikme_dolandyryş.server_close();raise
        자신.birikme_dolandyryş.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_port=자신.birikme_dolandyryş.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for serwer_baha in (자신.birikme_dolandyryş,자신.전문제어):
            작업가닥=threading.Thread(target=serwer_baha.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*argument_ARRAY):
        for serwer_baha in (자신.birikme_dolandyryş,자신.전문제어):serwer_baha.shutdown();serwer_baha.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    argument_ARRAY=인수해석기.parse_args()
    with 되돌림서버(argument_ARRAY.tcp_port,argument_ARRAY.udp_port) as 되돌림서버항목:
        print('esasy TCP {}, UDP {} Taýýarla. 게스트 salgy: 10.0.2.2. çyk_programma: Ctrl+C'.format(되돌림서버항목.TCP_port,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
