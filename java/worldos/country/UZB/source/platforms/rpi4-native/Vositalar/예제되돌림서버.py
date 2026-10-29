#!/usr/bin/env python3
"""한국어 네트워크 예제용 tashkilotchi TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,TCP_bayonnomasi_port=0,UDP_port=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);ma_lumotlar=bytearray()
                while b'\n' not in ma_lumotlar and len(ma_lumotlar)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    ma_lumotlar.extend(조각)
                수신됨.append(('tcp',bytes(ma_lumotlar)));자신.request.sendall(ma_lumotlar)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                ma_lumotlar,소켓=자신.request;수신됨.append(('udp',ma_lumotlar));소켓.sendto(ma_lumotlar,자신.client_address)
        자신.aloqa_boshqaruv=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_bayonnomasi_port),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_port),전문요청처리)
        except Exception:자신.aloqa_boshqaruv.server_close();raise
        자신.aloqa_boshqaruv.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_bayonnomasi_port=자신.aloqa_boshqaruv.server_address[1];자신.UDP_port=자신.전문제어.server_address[1]

    def __enter__(자신):
        for server_VALUE in (자신.aloqa_boshqaruv,자신.전문제어):
            작업가닥=threading.Thread(target=server_VALUE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*dalil_ARRAY):
        for server_VALUE in (자신.aloqa_boshqaruv,자신.전문제어):server_VALUE.shutdown();server_VALUE.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tcp-port',type=int,default=9000);parser.add_argument('--udp-port',type=int,default=9001)
    dalil_ARRAY=parser.parse_args()
    with 되돌림서버(dalil_ARRAY.tcp_port,dalil_ARRAY.udp_port) as 되돌림서버항목:
        print('tashkilotchi TCP {}, UDP {} Tayyorlamoq. 게스트 manzil: 10.0.2.2. Chiqish_ilova: Ctrl+C'.format(되돌림서버항목.TCP_bayonnomasi_port,되돌림서버항목.UDP_port),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
