#!/usr/bin/env python3
"""Lietuvių 네트워크 예제용 organizuoti TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class aidas_Serveriai:
    def __init__(자신,TCP_jungtis=0,UDP_jungtis=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class rodyklė_ryšys_užklausa(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);duomenys=bytearray()
                while b'\n' not in duomenys and len(duomenys)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    duomenys.extend(조각)
                수신됨.append(('tcp',bytes(duomenys)));자신.request.sendall(duomenys)
        class paketų_kelio_schema_rodyklė_užklausa(socketserver.BaseRequestHandler):
            def handle(자신):
                duomenys,소켓=자신.request;수신됨.append(('udp',duomenys));소켓.sendto(duomenys,자신.client_address)
        자신.ryšys_valdymas=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_jungtis),rodyklė_ryšys_užklausa)
        try:자신.paketų_kelio_schema_valdymas=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_jungtis),paketų_kelio_schema_rodyklė_užklausa)
        except Exception:자신.ryšys_valdymas.server_close();raise
        자신.ryšys_valdymas.daemon_threads=자신.paketų_kelio_schema_valdymas.daemon_threads=True
        자신.TCP_jungtis=자신.ryšys_valdymas.server_address[1];자신.UDP_jungtis=자신.paketų_kelio_schema_valdymas.server_address[1]

    def __enter__(자신):
        for serveris_VALUE in (자신.ryšys_valdymas,자신.paketų_kelio_schema_valdymas):
            darbininkas=threading.Thread(target=serveris_VALUE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            darbininkas.start();자신.작업가닥들.append(darbininkas)
        return 자신

    def __exit__(자신,*argumentas_ARRAY):
        for serveris_VALUE in (자신.ryšys_valdymas,자신.paketų_kelio_schema_valdymas):serveris_VALUE.shutdown();serveris_VALUE.server_close()
        for darbininkas in 자신.작업가닥들:darbininkas.join(timeout=1)


if __name__=='__main__':
    analizatorius=argparse.ArgumentParser(description=__doc__)
    analizatorius.add_argument('--tcp-port',type=int,default=9000);analizatorius.add_argument('--udp-port',type=int,default=9001)
    argumentas_ARRAY=analizatorius.parse_args()
    with aidas_Serveriai(argumentas_ARRAY.tcp_port,argumentas_ARRAY.udp_port) as aidas_serveris_įrašas:
        print('organizuoti TCP {}, UDP {} Parengti. 게스트 ADDRESS: 10.0.2.2. Baigti_programa_086bb533: Ctrl+C'.format(aidas_serveris_įrašas.TCP_jungtis,aidas_serveris_įrašas.UDP_jungtis),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
