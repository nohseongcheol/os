#!/usr/bin/env python3
"""Euskara 네트워크 예제용 Ostalari TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class atzeko_planoko_eguneratze_Zerbitzariak:
    def __init__(자신,TCP_ataka=0,UDP_ataka=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class helduleku_konexio_eskaera(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);datuak=bytearray()
                while b'\n' not in datuak and len(datuak)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    datuak.extend(조각)
                수신됨.append(('tcp',bytes(datuak)));자신.request.sendall(datuak)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                datuak,소켓=자신.request;수신됨.append(('udp',datuak));소켓.sendto(datuak,자신.client_address)
        자신.konexio_kontrol=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_ataka),helduleku_konexio_eskaera)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_ataka),전문요청처리)
        except Exception:자신.konexio_kontrol.server_close();raise
        자신.konexio_kontrol.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_ataka=자신.konexio_kontrol.server_address[1];자신.UDP_ataka=자신.전문제어.server_address[1]

    def __enter__(자신):
        for zerbitzari_balio in (자신.konexio_kontrol,자신.전문제어):
            작업가닥=threading.Thread(target=zerbitzari_balio.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*arg_matrize):
        for zerbitzari_balio in (자신.konexio_kontrol,자신.전문제어):zerbitzari_balio.shutdown();zerbitzari_balio.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    analizatzaile=argparse.ArgumentParser(description=__doc__)
    analizatzaile.add_argument('--tcp-port',type=int,default=9000);analizatzaile.add_argument('--udp-port',type=int,default=9001)
    arg_matrize=analizatzaile.parse_args()
    with atzeko_planoko_eguneratze_Zerbitzariak(arg_matrize.tcp_port,arg_matrize.udp_port) as atzeko_planoko_eguneratze_zerbitzari_sarrera:
        print('Ostalari TCP {}, UDP {} 준비. 게스트 helbide: 10.0.2.2. irten_aplik: Ctrl+C'.format(atzeko_planoko_eguneratze_zerbitzari_sarrera.TCP_ataka,atzeko_planoko_eguneratze_zerbitzari_sarrera.UDP_ataka),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
