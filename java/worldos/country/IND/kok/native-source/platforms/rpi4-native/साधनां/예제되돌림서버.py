#!/usr/bin/env python3
"""한국어 네트워크 예제용 येजमान TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,TCP_पोर्ट=0,UDP_पोर्ट=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);डेटा=bytearray()
                while b'\n' not in डेटा and len(डेटा)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    डेटा.extend(조각)
                수신됨.append(('tcp',bytes(डेटा)));자신.request.sendall(डेटा)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                डेटा,소켓=자신.request;수신됨.append(('udp',डेटा));소켓.sendto(डेटा,자신.client_address)
        자신.कनॅक्शन_नियंत्रण=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_पोर्ट),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_पोर्ट),전문요청처리)
        except Exception:자신.कनॅक्शन_नियंत्रण.server_close();raise
        자신.कनॅक्शन_नियंत्रण.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_पोर्ट=자신.कनॅक्शन_नियंत्रण.server_address[1];자신.UDP_पोर्ट=자신.전문제어.server_address[1]

    def __enter__(자신):
        for सर्वर_मोल in (자신.कनॅक्शन_नियंत्रण,자신.전문제어):
            작업가닥=threading.Thread(target=सर्वर_मोल.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*युक्तीवाद_क्रम):
        for सर्वर_मोल in (자신.कनॅक्शन_नियंत्रण,자신.전문제어):सर्वर_मोल.shutdown();सर्वर_मोल.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    युक्तीवाद_क्रम=인수해석기.parse_args()
    with 되돌림서버(युक्तीवाद_क्रम.tcp_port,युक्तीवाद_क्रम.udp_port) as 되돌림서버항목:
        print('येजमान TCP {}, UDP {} तयार_करचें_9ce364fc. 게스트 नामो: 10.0.2.2. प्रस्थान_करचें_एप्लिकेशन: Ctrl+C'.format(되돌림서버항목.TCP_पोर्ट,되돌림서버항목.UDP_पोर्ट),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
