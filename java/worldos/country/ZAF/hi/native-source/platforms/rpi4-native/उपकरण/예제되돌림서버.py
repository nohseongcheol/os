#!/usr/bin/env python3
"""हिंदी 네트워크 예제용 आयोजक TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class प्रतिध्वनि_सर्वर:
    def __init__(자신,연결접속번호=0,यूज़र_डेटाग्राम_प्रॉटोकॉल_पोर्ट=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class हैंडल_कनेक्शन_अनुरोध(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);आँकड़े=bytearray()
                while b'\n' not in आँकड़े and len(आँकड़े)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    आँकड़े.extend(조각)
                수신됨.append(('tcp',bytes(आँकड़े)));자신.request.sendall(आँकड़े)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                आँकड़े,सॉकेट_मान=자신.request;수신됨.append(('udp',आँकड़े));सॉकेट_मान.sendto(आँकड़े,자신.client_address)
        자신.कनेक्शन_नियंत्रण=socketserver.ThreadingTCPServer(('127.0.0.1',연결접속번호),हैंडल_कनेक्शन_अनुरोध)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',यूज़र_डेटाग्राम_प्रॉटोकॉल_पोर्ट),전문요청처리)
        except Exception:자신.कनेक्शन_नियंत्रण.server_close();raise
        자신.कनेक्शन_नियंत्रण.daemon_threads=자신.전문제어.daemon_threads=True
        자신.연결접속번호=자신.कनेक्शन_नियंत्रण.server_address[1];자신.यूज़र_डेटाग्राम_प्रॉटोकॉल_पोर्ट=자신.전문제어.server_address[1]

    def __enter__(자신):
        for 서버 in (자신.कनेक्शन_नियंत्रण,자신.전문제어):
            कार्यसूत्र=threading.Thread(target=서버.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            कार्यसूत्र.start();자신.작업가닥들.append(कार्यसूत्र)
        return 자신

    def __exit__(자신,*तर्क_सरणी):
        for 서버 in (자신.कनेक्शन_नियंत्रण,자신.전문제어):서버.shutdown();서버.server_close()
        for कार्यसूत्र in 자신.작업가닥들:कार्यसूत्र.join(timeout=1)


if __name__=='__main__':
    पार्सर=argparse.ArgumentParser(description=__doc__)
    पार्सर.add_argument('--tcp-port',type=int,default=9000);पार्सर.add_argument('--udp-port',type=int,default=9001)
    तर्क_सरणी=पार्सर.parse_args()
    with प्रतिध्वनि_सर्वर(तर्क_सरणी.tcp_port,तर्क_सरणी.udp_port) as 되돌림서버항목:
        print('आयोजक TCP {}, UDP {} 준비. 게스트 पता: 10.0.2.2. निर्गमन_ऐप: Ctrl+C'.format(되돌림서버항목.연결접속번호,되돌림서버항목.यूज़र_डेटाग्राम_प्रॉटोकॉल_पोर्ट),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
