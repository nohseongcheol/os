#!/usr/bin/env python3
"""Melayu 네트워크 예제용 hos TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,TCP_port=0,UDP_port=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class pemegang_hubungan_permintaan(socketserver.BaseRequestHandler):
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
        자신.hubungan_kawalan=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_port),pemegang_hubungan_permintaan)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_port),전문요청처리)
        except Exception:자신.hubungan_kawalan.server_close();raise
        자신.hubungan_kawalan.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_port=자신.hubungan_kawalan.server_address[1];자신.UDP_port=자신.전문제어.server_address[1]

    def __enter__(자신):
        for pelayan_VALUE in (자신.hubungan_kawalan,자신.전문제어):
            작업가닥=threading.Thread(target=pelayan_VALUE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*argumen_ARRAY):
        for pelayan_VALUE in (자신.hubungan_kawalan,자신.전문제어):pelayan_VALUE.shutdown();pelayan_VALUE.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    penghurai=argparse.ArgumentParser(description=__doc__)
    penghurai.add_argument('--tcp-port',type=int,default=9000);penghurai.add_argument('--udp-port',type=int,default=9001)
    argumen_ARRAY=penghurai.parse_args()
    with 되돌림서버(argumen_ARRAY.tcp_port,argumen_ARRAY.udp_port) as 되돌림서버항목:
        print('hos TCP {}, UDP {} Sediakan. 게스트 e_mel: 10.0.2.2. Keluar_aplikasi: Ctrl+C'.format(되돌림서버항목.TCP_port,되돌림서버항목.UDP_port),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
