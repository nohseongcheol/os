#!/usr/bin/env python3
"""한국어 네트워크 예제용 go_nea_ditirelo TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,TCP_phote=0,전문접속번호=0):
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
        자신.kgokaganya_taolo=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_phote),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.kgokaganya_taolo.server_close();raise
        자신.kgokaganya_taolo.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_phote=자신.kgokaganya_taolo.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for seba_boleng in (자신.kgokaganya_taolo,자신.전문제어):
            작업가닥=threading.Thread(target=seba_boleng.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*akumente_arei):
        for seba_boleng in (자신.kgokaganya_taolo,자신.전문제어):seba_boleng.shutdown();seba_boleng.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    akumente_arei=인수해석기.parse_args()
    with 되돌림서버(akumente_arei.tcp_port,akumente_arei.udp_port) as 되돌림서버항목:
        print('go_nea_ditirelo TCP {}, UDP {} Lokišetša. 게스트 atrese: 10.0.2.2. Etšwa_tirišo: Ctrl+C'.format(되돌림서버항목.TCP_phote,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
