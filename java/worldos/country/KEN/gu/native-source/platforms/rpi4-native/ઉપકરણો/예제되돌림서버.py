#!/usr/bin/env python3
"""ગુજરાતી 네트워크 예제용 હોસ્ટ TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,પ્રસારણ_નિયંત્રણ_પ્રોટોકૉલ_પૉર્ટ=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);ડેટા=bytearray()
                while b'\n' not in ડેટા and len(ડેટા)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    ડેટા.extend(조각)
                수신됨.append(('tcp',bytes(ડેટા)));자신.request.sendall(ડેટા)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                ડેટા,소켓=자신.request;수신됨.append(('udp',ડેટા));소켓.sendto(ડેટા,자신.client_address)
        자신.કનેક્શન_નિયંત્રણ=socketserver.ThreadingTCPServer(('127.0.0.1',પ્રસારણ_નિયંત્રણ_પ્રોટોકૉલ_પૉર્ટ),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.કનેક્શન_નિયંત્રણ.server_close();raise
        자신.કનેક્શન_નિયંત્રણ.daemon_threads=자신.전문제어.daemon_threads=True
        자신.પ્રસારણ_નિયંત્રણ_પ્રોટોકૉલ_પૉર્ટ=자신.કનેક્શન_નિયંત્રણ.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for સર્વર_મૂલ્ય in (자신.કનેક્શન_નિયંત્રણ,자신.전문제어):
            작업가닥=threading.Thread(target=સર્વર_મૂલ્ય.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*દલીલ_અરે):
        for સર્વર_મૂલ્ય in (자신.કનેક્શન_નિયંત્રણ,자신.전문제어):સર્વર_મૂલ્ય.shutdown();સર્વર_મૂલ્ય.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    દલીલ_અરે=인수해석기.parse_args()
    with 되돌림서버(દલીલ_અરે.tcp_port,દલીલ_અરે.udp_port) as 되돌림서버항목:
        print('હોસ્ટ TCP {}, UDP {} તૈયાર_કરો. 게스트 સરનામું: 10.0.2.2. પ્રસ્થાન_એપ્લિકેશન: Ctrl+C'.format(되돌림서버항목.પ્રસારણ_નિયંત્રણ_પ્રોટોકૉલ_પૉર્ટ,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
