#!/usr/bin/env python3
"""नेपाली 네트워크 예제용 होस्ट TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,टिसिपी_पोर्ट=0,युडिपी_पोर्ट=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);लगत=bytearray()
                while b'\n' not in लगत and len(लगत)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    लगत.extend(조각)
                수신됨.append(('tcp',bytes(लगत)));자신.request.sendall(लगत)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                लगत,소켓=자신.request;수신됨.append(('udp',लगत));소켓.sendto(लगत,자신.client_address)
        자신.जडान_नियन्त्रण=socketserver.ThreadingTCPServer(('127.0.0.1',टिसिपी_पोर्ट),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',युडिपी_पोर्ट),전문요청처리)
        except Exception:자신.जडान_नियन्त्रण.server_close();raise
        자신.जडान_नियन्त्रण.daemon_threads=자신.전문제어.daemon_threads=True
        자신.टिसिपी_पोर्ट=자신.जडान_नियन्त्रण.server_address[1];자신.युडिपी_पोर्ट=자신.전문제어.server_address[1]

    def __enter__(자신):
        for सर्भर_मान in (자신.जडान_नियन्त्रण,자신.전문제어):
            작업가닥=threading.Thread(target=सर्भर_मान.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*तर्क_विन्यास):
        for सर्भर_मान in (자신.जडान_नियन्त्रण,자신.전문제어):सर्भर_मान.shutdown();सर्भर_मान.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    तर्क_विन्यास=인수해석기.parse_args()
    with 되돌림서버(तर्क_विन्यास.tcp_port,तर्क_विन्यास.udp_port) as 되돌림서버항목:
        print('होस्ट TCP {}, UDP {} तयार_गर्नुहोस्. 게스트 ठेगाना: 10.0.2.2. बाहिर_जानुहोस्_अनुप्रयोग: Ctrl+C'.format(되돌림서버항목.टिसिपी_पोर्ट,되돌림서버항목.युडिपी_पोर्ट),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
