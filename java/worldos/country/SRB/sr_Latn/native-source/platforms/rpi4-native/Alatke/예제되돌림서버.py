#!/usr/bin/env python3
"""한국어 네트워크 예제용 host TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class eho_Serveri:
    def __init__(자신,TCP_port=0,UDP_port=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class pokazivač_veza_zahtev(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);podaci=bytearray()
                while b'\n' not in podaci and len(podaci)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    podaci.extend(조각)
                수신됨.append(('tcp',bytes(podaci)));자신.request.sendall(podaci)
        class datagram_pokazivač_zahtev(socketserver.BaseRequestHandler):
            def handle(자신):
                podaci,소켓=자신.request;수신됨.append(('udp',podaci));소켓.sendto(podaci,자신.client_address)
        자신.veza_kontrola=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_port),pokazivač_veza_zahtev)
        try:자신.datagram_kontrola=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_port),datagram_pokazivač_zahtev)
        except Exception:자신.veza_kontrola.server_close();raise
        자신.veza_kontrola.daemon_threads=자신.datagram_kontrola.daemon_threads=True
        자신.TCP_port=자신.veza_kontrola.server_address[1];자신.UDP_port=자신.datagram_kontrola.server_address[1]

    def __enter__(자신):
        for server_VALUE in (자신.veza_kontrola,자신.datagram_kontrola):
            작업가닥=threading.Thread(target=server_VALUE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*argument_niz):
        for server_VALUE in (자신.veza_kontrola,자신.datagram_kontrola):server_VALUE.shutdown();server_VALUE.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    analizator=argparse.ArgumentParser(description=__doc__)
    analizator.add_argument('--tcp-port',type=int,default=9000);analizator.add_argument('--udp-port',type=int,default=9001)
    argument_niz=analizator.parse_args()
    with eho_Serveri(argument_niz.tcp_port,argument_niz.udp_port) as eho_server_stavka:
        print('host TCP {}, UDP {} Pripremi. 게스트 adresa: 10.0.2.2. Izađi_program: Ctrl+C'.format(eho_server_stavka.TCP_port,eho_server_stavka.UDP_port),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
