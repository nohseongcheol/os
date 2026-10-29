#!/usr/bin/env python3
"""한국어 네트워크 예제용 sauka TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,TCP_fot=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);Tarin_bayani=bytearray()
                while b'\n' not in Tarin_bayani and len(Tarin_bayani)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    Tarin_bayani.extend(조각)
                수신됨.append(('tcp',bytes(Tarin_bayani)));자신.request.sendall(Tarin_bayani)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                Tarin_bayani,소켓=자신.request;수신됨.append(('udp',Tarin_bayani));소켓.sendto(Tarin_bayani,자신.client_address)
        자신.haɗi_masarrafa=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_fot),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.haɗi_masarrafa.server_close();raise
        자신.haɗi_masarrafa.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_fot=자신.haɗi_masarrafa.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for Saba_Daraja in (자신.haɗi_masarrafa,자신.전문제어):
            작업가닥=threading.Thread(target=Saba_Daraja.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*Tubalin_aiki_TSARI):
        for Saba_Daraja in (자신.haɗi_masarrafa,자신.전문제어):Saba_Daraja.shutdown();Saba_Daraja.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    tatsar_manhaja=argparse.ArgumentParser(description=__doc__)
    tatsar_manhaja.add_argument('--tcp-port',type=int,default=9000);tatsar_manhaja.add_argument('--udp-port',type=int,default=9001)
    Tubalin_aiki_TSARI=tatsar_manhaja.parse_args()
    with 되돌림서버(Tubalin_aiki_TSARI.tcp_port,Tubalin_aiki_TSARI.udp_port) as 되돌림서버항목:
        print('sauka TCP {}, UDP {} Shirya. 게스트 imel: 10.0.2.2. Mafita_Shiri: Ctrl+C'.format(되돌림서버항목.TCP_fot,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
