#!/usr/bin/env python3
"""Italiano 네트워크 예제용 host TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class eco_schermo_Server:
    def __init__(자신,porta_TCP=0,UDP_porta=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class handle_connessione_richiesta(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);dati=bytearray()
                while b'\n' not in dati and len(dati)<=512:
                    blocco_VALORE_652d4b53=자신.request.recv(512)
                    if not blocco_VALORE_652d4b53:return
                    dati.extend(blocco_VALORE_652d4b53)
                수신됨.append(('tcp',bytes(dati)));자신.request.sendall(dati)
        class datagramma_handle_richiesta(socketserver.BaseRequestHandler):
            def handle(자신):
                dati,socket_VALORE=자신.request;수신됨.append(('udp',dati));socket_VALORE.sendto(dati,자신.client_address)
        자신.connessione_controllo=socketserver.ThreadingTCPServer(('127.0.0.1',porta_TCP),handle_connessione_richiesta)
        try:자신.datagramma_controllo=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_porta),datagramma_handle_richiesta)
        except Exception:자신.connessione_controllo.server_close();raise
        자신.connessione_controllo.daemon_threads=자신.datagramma_controllo.daemon_threads=True
        자신.porta_TCP=자신.connessione_controllo.server_address[1];자신.UDP_porta=자신.datagramma_controllo.server_address[1]

    def __enter__(자신):
        for server_VALORE in (자신.connessione_controllo,자신.datagramma_controllo):
            esecutoreAsincrono=threading.Thread(target=server_VALORE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            esecutoreAsincrono.start();자신.작업가닥들.append(esecutoreAsincrono)
        return 자신

    def __exit__(자신,*argomento_array):
        for server_VALORE in (자신.connessione_controllo,자신.datagramma_controllo):server_VALORE.shutdown();server_VALORE.server_close()
        for esecutoreAsincrono in 자신.작업가닥들:esecutoreAsincrono.join(timeout=1)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tcp-port',type=int,default=9000);parser.add_argument('--udp-port',type=int,default=9001)
    argomento_array=parser.parse_args()
    with eco_schermo_Server(argomento_array.tcp_port,argomento_array.udp_port) as eco_schermo_server_voce:
        print('host TCP {}, UDP {} Prepara. 게스트 e_mail: 10.0.2.2. Esci_app: Ctrl+C'.format(eco_schermo_server_voce.porta_TCP,eco_schermo_server_voce.UDP_porta),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
