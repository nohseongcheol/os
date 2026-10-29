#!/usr/bin/env python3
"""Slovenský 네트워크 예제용 hostiteľ TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class ozvena_Servery:
    def __init__(자신,TCP_port=0,UDP_port=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class rukoväť_kontakt_požiadavka(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);údaje=bytearray()
                while b'\n' not in údaje and len(údaje)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    údaje.extend(조각)
                수신됨.append(('tcp',bytes(údaje)));자신.request.sendall(údaje)
        class datagram_rukoväť_požiadavka(socketserver.BaseRequestHandler):
            def handle(자신):
                údaje,soket_VALUE=자신.request;수신됨.append(('udp',údaje));soket_VALUE.sendto(údaje,자신.client_address)
        자신.kontakt_riadenie=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_port),rukoväť_kontakt_požiadavka)
        try:자신.datagram_riadenie=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_port),datagram_rukoväť_požiadavka)
        except Exception:자신.kontakt_riadenie.server_close();raise
        자신.kontakt_riadenie.daemon_threads=자신.datagram_riadenie.daemon_threads=True
        자신.TCP_port=자신.kontakt_riadenie.server_address[1];자신.UDP_port=자신.datagram_riadenie.server_address[1]

    def __enter__(자신):
        for server_VALUE in (자신.kontakt_riadenie,자신.datagram_riadenie):
            작업가닥=threading.Thread(target=server_VALUE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*argument_pole):
        for server_VALUE in (자신.kontakt_riadenie,자신.datagram_riadenie):server_VALUE.shutdown();server_VALUE.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    analyzátor=argparse.ArgumentParser(description=__doc__)
    analyzátor.add_argument('--tcp-port',type=int,default=9000);analyzátor.add_argument('--udp-port',type=int,default=9001)
    argument_pole=analyzátor.parse_args()
    with ozvena_Servery(argument_pole.tcp_port,argument_pole.udp_port) as ozvena_server_položka:
        print('hostiteľ TCP {}, UDP {} Pripraviť. 게스트 adresa: 10.0.2.2. Skončiť_program: Ctrl+C'.format(ozvena_server_položka.TCP_port,ozvena_server_položka.UDP_port),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
