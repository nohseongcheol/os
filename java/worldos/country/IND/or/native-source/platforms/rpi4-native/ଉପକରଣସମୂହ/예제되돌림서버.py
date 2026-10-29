#!/usr/bin/env python3
"""한국어 네트워크 예제용 ଆୟୋଜକ TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,ପ୍ରେରଣ_ନିୟନ୍ତ୍ରଣ_ପ୍ରୋଟୋକଲ୍_ପୋର୍ଟ=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);ଡାଟା=bytearray()
                while b'\n' not in ଡାଟା and len(ଡାଟା)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    ଡାଟା.extend(조각)
                수신됨.append(('tcp',bytes(ଡାଟା)));자신.request.sendall(ଡାଟା)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                ଡାଟା,소켓=자신.request;수신됨.append(('udp',ଡାଟା));소켓.sendto(ଡାଟା,자신.client_address)
        자신.ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ=socketserver.ThreadingTCPServer(('127.0.0.1',ପ୍ରେରଣ_ନିୟନ୍ତ୍ରଣ_ପ୍ରୋଟୋକଲ୍_ପୋର୍ଟ),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ.server_close();raise
        자신.ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ.daemon_threads=자신.전문제어.daemon_threads=True
        자신.ପ୍ରେରଣ_ନିୟନ୍ତ୍ରଣ_ପ୍ରୋଟୋକଲ୍_ପୋର୍ଟ=자신.ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for ସର୍ଭର୍_ମୂଲ୍ୟ in (자신.ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ,자신.전문제어):
            작업가닥=threading.Thread(target=ସର୍ଭର୍_ମୂଲ୍ୟ.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*ଯୁକ୍ତି_ଆରେ):
        for ସର୍ଭର୍_ମୂଲ୍ୟ in (자신.ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ,자신.전문제어):ସର୍ଭର୍_ମୂଲ୍ୟ.shutdown();ସର୍ଭର୍_ମୂଲ୍ୟ.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    ଯୁକ୍ତି_ଆରେ=인수해석기.parse_args()
    with 되돌림서버(ଯୁକ୍ତି_ଆରେ.tcp_port,ଯୁକ୍ତି_ଆରେ.udp_port) as 되돌림서버항목:
        print('ଆୟୋଜକ TCP {}, UDP {} ପ୍ରସ୍ତୁତ. 게스트 ଠିକଣା: 10.0.2.2. ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ: Ctrl+C'.format(되돌림서버항목.ପ୍ରେରଣ_ନିୟନ୍ତ୍ରଣ_ପ୍ରୋଟୋକଲ୍_ପୋର୍ଟ,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
