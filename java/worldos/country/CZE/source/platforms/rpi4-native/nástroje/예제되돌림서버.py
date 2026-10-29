#!/usr/bin/env python3
"""čeština 네트워크 예제용 hostit TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class zobrazení_výsledků_Servery:
    def __init__(자신,port_TCP=0,protokol_UDP_port=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class úchyt_kontakt_žádost(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);data=bytearray()
                while b'\n' not in data and len(data)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    data.extend(조각)
                수신됨.append(('tcp',bytes(data)));자신.request.sendall(data)
        class datagram_úchyt_žádost(socketserver.BaseRequestHandler):
            def handle(자신):
                data,soket_HODNOTA=자신.request;수신됨.append(('udp',data));soket_HODNOTA.sendto(data,자신.client_address)
        자신.kontakt_řízení=socketserver.ThreadingTCPServer(('127.0.0.1',port_TCP),úchyt_kontakt_žádost)
        try:자신.datagram_řízení=socketserver.ThreadingUDPServer(('127.0.0.1',protokol_UDP_port),datagram_úchyt_žádost)
        except Exception:자신.kontakt_řízení.server_close();raise
        자신.kontakt_řízení.daemon_threads=자신.datagram_řízení.daemon_threads=True
        자신.port_TCP=자신.kontakt_řízení.server_address[1];자신.protokol_UDP_port=자신.datagram_řízení.server_address[1]

    def __enter__(자신):
        for server_HODNOTA in (자신.kontakt_řízení,자신.datagram_řízení):
            pracovník=threading.Thread(target=server_HODNOTA.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            pracovník.start();자신.작업가닥들.append(pracovník)
        return 자신

    def __exit__(자신,*argument_pole):
        for server_HODNOTA in (자신.kontakt_řízení,자신.datagram_řízení):server_HODNOTA.shutdown();server_HODNOTA.server_close()
        for pracovník in 자신.작업가닥들:pracovník.join(timeout=1)


if __name__=='__main__':
    analyzátor=argparse.ArgumentParser(description=__doc__)
    analyzátor.add_argument('--tcp-port',type=int,default=9000);analyzátor.add_argument('--udp-port',type=int,default=9001)
    argument_pole=analyzátor.parse_args()
    with zobrazení_výsledků_Servery(argument_pole.tcp_port,argument_pole.udp_port) as zobrazení_výsledků_server_položka:
        print('hostit TCP {}, UDP {} Připravit. 게스트 Adresa: 10.0.2.2. Konec_program: Ctrl+C'.format(zobrazení_výsledků_server_položka.port_TCP,zobrazení_výsledků_server_položka.protokol_UDP_port),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
