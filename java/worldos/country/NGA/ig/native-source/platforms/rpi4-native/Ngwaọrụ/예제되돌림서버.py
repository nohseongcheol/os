#!/usr/bin/env python3
"""한국어 네트워크 예제용 usu TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,TCP_pọọt=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);datà=bytearray()
                while b'\n' not in datà and len(datà)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    datà.extend(조각)
                수신됨.append(('tcp',bytes(datà)));자신.request.sendall(datà)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                datà,소켓=자신.request;수신됨.append(('udp',datà));소켓.sendto(datà,자신.client_address)
        자신.njikọ_njizi=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_pọọt),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.njikọ_njizi.server_close();raise
        자신.njikọ_njizi.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_pọọt=자신.njikọ_njizi.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for savà_valuu in (자신.njikọ_njizi,자신.전문제어):
            작업가닥=threading.Thread(target=savà_valuu.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*agụment_MKPOKỌTA):
        for savà_valuu in (자신.njikọ_njizi,자신.전문제어):savà_valuu.shutdown();savà_valuu.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    agụment_MKPOKỌTA=인수해석기.parse_args()
    with 되돌림서버(agụment_MKPOKỌTA.tcp_port,agụment_MKPOKỌTA.udp_port) as 되돌림서버항목:
        print('usu TCP {}, UDP {} Kwado. 게스트 àdreèsì: 10.0.2.2. pụọ_app: Ctrl+C'.format(되돌림서버항목.TCP_pọọt,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
