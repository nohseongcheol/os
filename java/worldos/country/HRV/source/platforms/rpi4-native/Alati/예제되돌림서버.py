#!/usr/bin/env python3
"""hrvatski 네트워크 예제용 domaćin TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class eho_Poslužitelji:
    def __init__(자신,TCP_prebaciti=0,UDP_prebaciti=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class ustroj_veza_zahtjev(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);podaci=bytearray()
                while b'\n' not in podaci and len(podaci)<=512:
                    fragment_VALUE=자신.request.recv(512)
                    if not fragment_VALUE:return
                    podaci.extend(fragment_VALUE)
                수신됨.append(('tcp',bytes(podaci)));자신.request.sendall(podaci)
        class datogram_ustroj_zahtjev(socketserver.BaseRequestHandler):
            def handle(자신):
                podaci,소켓=자신.request;수신됨.append(('udp',podaci));소켓.sendto(podaci,자신.client_address)
        자신.veza_kontrola=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_prebaciti),ustroj_veza_zahtjev)
        try:자신.datogram_kontrola=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_prebaciti),datogram_ustroj_zahtjev)
        except Exception:자신.veza_kontrola.server_close();raise
        자신.veza_kontrola.daemon_threads=자신.datogram_kontrola.daemon_threads=True
        자신.TCP_prebaciti=자신.veza_kontrola.server_address[1];자신.UDP_prebaciti=자신.datogram_kontrola.server_address[1]

    def __enter__(자신):
        for server_VALUE in (자신.veza_kontrola,자신.datogram_kontrola):
            작업가닥=threading.Thread(target=server_VALUE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*argument_ARRAY):
        for server_VALUE in (자신.veza_kontrola,자신.datogram_kontrola):server_VALUE.shutdown();server_VALUE.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    analizator=argparse.ArgumentParser(description=__doc__)
    analizator.add_argument('--tcp-port',type=int,default=9000);analizator.add_argument('--udp-port',type=int,default=9001)
    argument_ARRAY=analizator.parse_args()
    with eho_Poslužitelji(argument_ARRAY.tcp_port,argument_ARRAY.udp_port) as eho_server_unos:
        print('domaćin TCP {}, UDP {} Pripremi. 게스트 adresa: 10.0.2.2. Izlaz_program: Ctrl+C'.format(eho_server_unos.TCP_prebaciti,eho_server_unos.UDP_prebaciti),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
