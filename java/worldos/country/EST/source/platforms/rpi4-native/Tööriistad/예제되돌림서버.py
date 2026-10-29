#!/usr/bin/env python3
"""Eesti 네트워크 예제용 host TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class kaja_Serverid:
    def __init__(자신,TCP_port=0,UDP_port=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class pide_ühendus_päring(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);andmed=bytearray()
                while b'\n' not in andmed and len(andmed)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    andmed.extend(조각)
                수신됨.append(('tcp',bytes(andmed)));자신.request.sendall(andmed)
        class datagramm_pide_päring(socketserver.BaseRequestHandler):
            def handle(자신):
                andmed,소켓=자신.request;수신됨.append(('udp',andmed));소켓.sendto(andmed,자신.client_address)
        자신.ühendus_meede=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_port),pide_ühendus_päring)
        try:자신.datagramm_meede=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_port),datagramm_pide_päring)
        except Exception:자신.ühendus_meede.server_close();raise
        자신.ühendus_meede.daemon_threads=자신.datagramm_meede.daemon_threads=True
        자신.TCP_port=자신.ühendus_meede.server_address[1];자신.UDP_port=자신.datagramm_meede.server_address[1]

    def __enter__(자신):
        for server_VALUE in (자신.ühendus_meede,자신.datagramm_meede):
            töötaja=threading.Thread(target=server_VALUE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            töötaja.start();자신.작업가닥들.append(töötaja)
        return 자신

    def __exit__(자신,*argument_ARRAY):
        for server_VALUE in (자신.ühendus_meede,자신.datagramm_meede):server_VALUE.shutdown();server_VALUE.server_close()
        for töötaja in 자신.작업가닥들:töötaja.join(timeout=1)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tcp-port',type=int,default=9000);parser.add_argument('--udp-port',type=int,default=9001)
    argument_ARRAY=parser.parse_args()
    with kaja_Serverid(argument_ARRAY.tcp_port,argument_ARRAY.udp_port) as kaja_server_kirje:
        print('host TCP {}, UDP {} Ettevalmistamine. 게스트 ADDRESS: 10.0.2.2. Välju_programm: Ctrl+C'.format(kaja_server_kirje.TCP_port,kaja_server_kirje.UDP_port),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
