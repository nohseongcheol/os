#!/usr/bin/env python3
"""Latviešu 네트워크 예제용 viesot TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class atbalss_Serveri:
    def __init__(자신,TCP_ports=0,UDP_ports=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class turis_paziņa_pieprasījums(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);dati=bytearray()
                while b'\n' not in dati and len(dati)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    dati.extend(조각)
                수신됨.append(('tcp',bytes(dati)));자신.request.sendall(dati)
        class datogramma_turis_pieprasījums(socketserver.BaseRequestHandler):
            def handle(자신):
                dati,소켓=자신.request;수신됨.append(('udp',dati));소켓.sendto(dati,자신.client_address)
        자신.paziņa_vadība=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_ports),turis_paziņa_pieprasījums)
        try:자신.datogramma_vadība=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_ports),datogramma_turis_pieprasījums)
        except Exception:자신.paziņa_vadība.server_close();raise
        자신.paziņa_vadība.daemon_threads=자신.datogramma_vadība.daemon_threads=True
        자신.TCP_ports=자신.paziņa_vadība.server_address[1];자신.UDP_ports=자신.datogramma_vadība.server_address[1]

    def __enter__(자신):
        for serveris_VALUE in (자신.paziņa_vadība,자신.datogramma_vadība):
            nodarbinātais=threading.Thread(target=serveris_VALUE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            nodarbinātais.start();자신.작업가닥들.append(nodarbinātais)
        return 자신

    def __exit__(자신,*arg_ARRAY):
        for serveris_VALUE in (자신.paziņa_vadība,자신.datogramma_vadība):serveris_VALUE.shutdown();serveris_VALUE.server_close()
        for nodarbinātais in 자신.작업가닥들:nodarbinātais.join(timeout=1)


if __name__=='__main__':
    parsētājs=argparse.ArgumentParser(description=__doc__)
    parsētājs.add_argument('--tcp-port',type=int,default=9000);parsētājs.add_argument('--udp-port',type=int,default=9001)
    arg_ARRAY=parsētājs.parse_args()
    with atbalss_Serveri(arg_ARRAY.tcp_port,arg_ARRAY.udp_port) as atbalss_serveris_ievade:
        print('viesot TCP {}, UDP {} Sagatavot. 게스트 adrese: 10.0.2.2. Iziet_programma: Ctrl+C'.format(atbalss_serveris_ievade.TCP_ports,atbalss_serveris_ievade.UDP_ports),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
