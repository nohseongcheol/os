#!/usr/bin/env python3
"""Nederlands 네트워크 예제용 host TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class echo_Servers:
    def __init__(자신,TCP_poort=0,UDP_poort=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class greep_verbinding_aanvraag(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);gegevens=bytearray()
                while b'\n' not in gegevens and len(gegevens)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    gegevens.extend(조각)
                수신됨.append(('tcp',bytes(gegevens)));자신.request.sendall(gegevens)
        class datagram_greep_aanvraag(socketserver.BaseRequestHandler):
            def handle(자신):
                gegevens,socket_WAARDE=자신.request;수신됨.append(('udp',gegevens));socket_WAARDE.sendto(gegevens,자신.client_address)
        자신.verbinding_controle=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_poort),greep_verbinding_aanvraag)
        try:자신.datagram_controle=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_poort),datagram_greep_aanvraag)
        except Exception:자신.verbinding_controle.server_close();raise
        자신.verbinding_controle.daemon_threads=자신.datagram_controle.daemon_threads=True
        자신.TCP_poort=자신.verbinding_controle.server_address[1];자신.UDP_poort=자신.datagram_controle.server_address[1]

    def __enter__(자신):
        for server_WAARDE in (자신.verbinding_controle,자신.datagram_controle):
            achtergrondwerker=threading.Thread(target=server_WAARDE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            achtergrondwerker.start();자신.작업가닥들.append(achtergrondwerker)
        return 자신

    def __exit__(자신,*argument_MATRIX):
        for server_WAARDE in (자신.verbinding_controle,자신.datagram_controle):server_WAARDE.shutdown();server_WAARDE.server_close()
        for achtergrondwerker in 자신.작업가닥들:achtergrondwerker.join(timeout=1)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tcp-port',type=int,default=9000);parser.add_argument('--udp-port',type=int,default=9001)
    argument_MATRIX=parser.parse_args()
    with echo_Servers(argument_MATRIX.tcp_port,argument_MATRIX.udp_port) as echo_server_invoer:
        print('host TCP {}, UDP {} Bereid_voor. 게스트 ADRES: 10.0.2.2. Einde_app: Ctrl+C'.format(echo_server_invoer.TCP_poort,echo_server_invoer.UDP_poort),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
