#!/usr/bin/env python3
"""slovenščina 네트워크 예제용 gostiti TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class odmev_Strežniki:
    def __init__(자신,TCP_vrata=0,UDP_vrata=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class ročica_povezava_zahteva(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);podatki=bytearray()
                while b'\n' not in podatki and len(podatki)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    podatki.extend(조각)
                수신됨.append(('tcp',bytes(podatki)));자신.request.sendall(podatki)
        class datagram_ročica_zahteva(socketserver.BaseRequestHandler):
            def handle(자신):
                podatki,vtičnica_VALUE=자신.request;수신됨.append(('udp',podatki));vtičnica_VALUE.sendto(podatki,자신.client_address)
        자신.povezava_nadzor=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_vrata),ročica_povezava_zahteva)
        try:자신.datagram_nadzor=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_vrata),datagram_ročica_zahteva)
        except Exception:자신.povezava_nadzor.server_close();raise
        자신.povezava_nadzor.daemon_threads=자신.datagram_nadzor.daemon_threads=True
        자신.TCP_vrata=자신.povezava_nadzor.server_address[1];자신.UDP_vrata=자신.datagram_nadzor.server_address[1]

    def __enter__(자신):
        for strežnik_VALUE in (자신.povezava_nadzor,자신.datagram_nadzor):
            작업가닥=threading.Thread(target=strežnik_VALUE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*argument_ARRAY):
        for strežnik_VALUE in (자신.povezava_nadzor,자신.datagram_nadzor):strežnik_VALUE.shutdown();strežnik_VALUE.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    razčlenjevalnik=argparse.ArgumentParser(description=__doc__)
    razčlenjevalnik.add_argument('--tcp-port',type=int,default=9000);razčlenjevalnik.add_argument('--udp-port',type=int,default=9001)
    argument_ARRAY=razčlenjevalnik.parse_args()
    with odmev_Strežniki(argument_ARRAY.tcp_port,argument_ARRAY.udp_port) as odmev_strežnik_vnos:
        print('gostiti TCP {}, UDP {} Pripravi. 게스트 naslov: 10.0.2.2. Izhod_aplikacija: Ctrl+C'.format(odmev_strežnik_vnos.TCP_vrata,odmev_strežnik_vnos.UDP_vrata),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
