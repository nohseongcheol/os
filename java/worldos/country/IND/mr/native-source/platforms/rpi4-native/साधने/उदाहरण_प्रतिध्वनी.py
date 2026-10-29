#!/usr/bin/env python3
"""मराठी 네트워크 예제용 होस्ट TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class प्रतिध्वनी_सर्व्हर्स:
    def __init__(स्वतः,ट्रान्समिशन_कंट्रोल_प्रोटोकॉल_पॉर्ट=0,स्वतंत्रसंदेशसंचार_पॉर्ट=0):
        स्वतः.आहे_स्वीकारलेले=[];स्वतः.कार्यसूत्रे=[]
        आहे_स्वीकारलेले=स्वतः.आहे_स्वीकारलेले
        class हाताळा_कनेक्शन_विनंती(socketserver.BaseRequestHandler):
            def handle(स्वतः):
                स्वतः.request.settimeout(5);डेटा=bytearray()
                while b'\n' not in डेटा and len(डेटा)<=512:
                    तुकडा_मूल्य=स्वतः.request.recv(512)
                    if not तुकडा_मूल्य:return
                    डेटा.extend(तुकडा_मूल्य)
                आहे_स्वीकारलेले.append(('tcp',bytes(डेटा)));स्वतः.request.sendall(डेटा)
        class स्वतंत्रसंदेश_हाताळा_विनंती(socketserver.BaseRequestHandler):
            def handle(स्वतः):
                डेटा,संचारद्वार_मूल्य=स्वतः.request;आहे_स्वीकारलेले.append(('udp',डेटा));संचारद्वार_मूल्य.sendto(डेटा,स्वतः.client_address)
        स्वतः.कनेक्शन_नियंत्रण=socketserver.ThreadingTCPServer(('127.0.0.1',ट्रान्समिशन_कंट्रोल_प्रोटोकॉल_पॉर्ट),हाताळा_कनेक्शन_विनंती)
        try:स्वतः.स्वतंत्रसंदेश_नियंत्रण=socketserver.ThreadingUDPServer(('127.0.0.1',स्वतंत्रसंदेशसंचार_पॉर्ट),स्वतंत्रसंदेश_हाताळा_विनंती)
        except Exception:स्वतः.कनेक्शन_नियंत्रण.server_close();raise
        स्वतः.कनेक्शन_नियंत्रण.daemon_threads=स्वतः.स्वतंत्रसंदेश_नियंत्रण.daemon_threads=True
        स्वतः.ट्रान्समिशन_कंट्रोल_प्रोटोकॉल_पॉर्ट=स्वतः.कनेक्शन_नियंत्रण.server_address[1];स्वतः.स्वतंत्रसंदेशसंचार_पॉर्ट=स्वतः.स्वतंत्रसंदेश_नियंत्रण.server_address[1]

    def __enter__(स्वतः):
        for सर्व्हर_मूल्य in (स्वतः.कनेक्शन_नियंत्रण,स्वतः.स्वतंत्रसंदेश_नियंत्रण):
            कार्यसूत्र=threading.Thread(target=सर्व्हर_मूल्य.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            कार्यसूत्र.start();स्वतः.कार्यसूत्रे.append(कार्यसूत्र)
        return स्वतः

    def __exit__(स्वतः,*वितर्क_ऍरे):
        for सर्व्हर_मूल्य in (स्वतः.कनेक्शन_नियंत्रण,स्वतः.स्वतंत्रसंदेश_नियंत्रण):सर्व्हर_मूल्य.shutdown();सर्व्हर_मूल्य.server_close()
        for कार्यसूत्र in स्वतः.कार्यसूत्रे:कार्यसूत्र.join(timeout=1)


if __name__=='__main__':
    व्याकरणविश्लेषक=argparse.ArgumentParser(description=__doc__)
    व्याकरणविश्लेषक.add_argument('--tcp-port',type=int,default=9000);व्याकरणविश्लेषक.add_argument('--udp-port',type=int,default=9001)
    वितर्क_ऍरे=व्याकरणविश्लेषक.parse_args()
    with प्रतिध्वनी_सर्व्हर्स(वितर्क_ऍरे.tcp_port,वितर्क_ऍरे.udp_port) as प्रतिध्वनी_सर्व्हर_प्रविष्टी:
        print('होस्ट TCP {}, UDP {} तयार_करणे. 게스트 पत्ता: 10.0.2.2. निर्गमन_करा_अनुप्रयोग: Ctrl+C'.format(प्रतिध्वनी_सर्व्हर_प्रविष्टी.ट्रान्समिशन_कंट्रोल_प्रोटोकॉल_पॉर्ट,प्रतिध्वनी_सर्व्हर_प्रविष्टी.स्वतंत्रसंदेशसंचार_पॉर्ट),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
