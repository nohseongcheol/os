#!/usr/bin/env python3
"""한국어 네트워크 예제용 호스트 TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,연결접속번호=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);자료=bytearray()
                while b'\n' not in 자료 and len(자료)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    자료.extend(조각)
                수신됨.append(('tcp',bytes(자료)));자신.request.sendall(자료)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자료,소켓=자신.request;수신됨.append(('udp',자료));소켓.sendto(자료,자신.client_address)
        자신.연결제어=socketserver.ThreadingTCPServer(('127.0.0.1',연결접속번호),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.연결제어.server_close();raise
        자신.연결제어.daemon_threads=자신.전문제어.daemon_threads=True
        자신.연결접속번호=자신.연결제어.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for 서버 in (자신.연결제어,자신.전문제어):
            작업가닥=threading.Thread(target=서버.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*인수배열):
        for 서버 in (자신.연결제어,자신.전문제어):서버.shutdown();서버.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    인수배열=인수해석기.parse_args()
    with 되돌림서버(인수배열.tcp_port,인수배열.udp_port) as 되돌림서버항목:
        print('호스트 TCP {}, UDP {} 준비. 게스트 주소: 10.0.2.2. 종료: Ctrl+C'.format(되돌림서버항목.연결접속번호,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
