#!/usr/bin/env python3
"""한국어 네트워크 예제용 হ_ষ্ট TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,প্রচাৰণ_নিয়ন্ত্রণ_প্ৰ_ট_ক_ল_পৰ্ট=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);ডাটা=bytearray()
                while b'\n' not in ডাটা and len(ডাটা)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    ডাটা.extend(조각)
                수신됨.append(('tcp',bytes(ডাটা)));자신.request.sendall(ডাটা)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                ডাটা,소켓=자신.request;수신됨.append(('udp',ডাটা));소켓.sendto(ডাটা,자신.client_address)
        자신.সংযোগ_নিয়ন্ত্রণ=socketserver.ThreadingTCPServer(('127.0.0.1',প্রচাৰণ_নিয়ন্ত্রণ_প্ৰ_ট_ক_ল_পৰ্ট),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.সংযোগ_নিয়ন্ত্রণ.server_close();raise
        자신.সংযোগ_নিয়ন্ত্রণ.daemon_threads=자신.전문제어.daemon_threads=True
        자신.প্রচাৰণ_নিয়ন্ত্রণ_প্ৰ_ট_ক_ল_পৰ্ট=자신.সংযোগ_নিয়ন্ত্রণ.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for ছাৰ্ভাৰ_মান in (자신.সংযোগ_নিয়ন্ত্রণ,자신.전문제어):
            작업가닥=threading.Thread(target=ছাৰ্ভাৰ_মান.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*যুক্তি_শৃঙ্খলা):
        for ছাৰ্ভাৰ_মান in (자신.সংযোগ_নিয়ন্ত্রণ,자신.전문제어):ছাৰ্ভাৰ_মান.shutdown();ছাৰ্ভাৰ_মান.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    যুক্তি_শৃঙ্খলা=인수해석기.parse_args()
    with 되돌림서버(যুক্তি_শৃঙ্খলা.tcp_port,যুক্তি_শৃঙ্খলা.udp_port) as 되돌림서버항목:
        print('হ_ষ্ট TCP {}, UDP {} প্ৰস্তুত_কৰক. 게스트 ঠিকনা: 10.0.2.2. প্ৰস্থান_এপ্প্: Ctrl+C'.format(되돌림서버항목.প্রচাৰণ_নিয়ন্ত্রণ_প্ৰ_ট_ক_ল_পৰ্ট,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
