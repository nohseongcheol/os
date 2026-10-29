#!/usr/bin/env python3
"""magyar 네트워크 예제용 gazda TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class visszhang_Kiszolgálók:
    def __init__(자신,TCP_port=0,UDP_port=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class leíró_ismerős_kérés(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);adat=bytearray()
                while b'\n' not in adat and len(adat)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    adat.extend(조각)
                수신됨.append(('tcp',bytes(adat)));자신.request.sendall(adat)
        class datagram_leíró_kérés(socketserver.BaseRequestHandler):
            def handle(자신):
                adat,szoftvercsatorna_ÉRTÉK=자신.request;수신됨.append(('udp',adat));szoftvercsatorna_ÉRTÉK.sendto(adat,자신.client_address)
        자신.ismerős_vezérlő=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_port),leíró_ismerős_kérés)
        try:자신.datagram_vezérlő=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_port),datagram_leíró_kérés)
        except Exception:자신.ismerős_vezérlő.server_close();raise
        자신.ismerős_vezérlő.daemon_threads=자신.datagram_vezérlő.daemon_threads=True
        자신.TCP_port=자신.ismerős_vezérlő.server_address[1];자신.UDP_port=자신.datagram_vezérlő.server_address[1]

    def __enter__(자신):
        for kiszolgáló_ÉRTÉK in (자신.ismerős_vezérlő,자신.datagram_vezérlő):
            dolgozó=threading.Thread(target=kiszolgáló_ÉRTÉK.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            dolgozó.start();자신.작업가닥들.append(dolgozó)
        return 자신

    def __exit__(자신,*argumentum_TÖMB):
        for kiszolgáló_ÉRTÉK in (자신.ismerős_vezérlő,자신.datagram_vezérlő):kiszolgáló_ÉRTÉK.shutdown();kiszolgáló_ÉRTÉK.server_close()
        for dolgozó in 자신.작업가닥들:dolgozó.join(timeout=1)


if __name__=='__main__':
    elemző=argparse.ArgumentParser(description=__doc__)
    elemző.add_argument('--tcp-port',type=int,default=9000);elemző.add_argument('--udp-port',type=int,default=9001)
    argumentum_TÖMB=elemző.parse_args()
    with visszhang_Kiszolgálók(argumentum_TÖMB.tcp_port,argumentum_TÖMB.udp_port) as visszhang_kiszolgáló_bejegyzés:
        print('gazda TCP {}, UDP {} Előkészítés. 게스트 CÍM: 10.0.2.2. kilép_app: Ctrl+C'.format(visszhang_kiszolgáló_bejegyzés.TCP_port,visszhang_kiszolgáló_bejegyzés.UDP_port),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
