#!/usr/bin/env python3
"""suomi 네트워크 예제용 isäntä TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class päivitys_Palvelimet:
    def __init__(자신,TCP_portti=0,UDP_portti=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class kahva_yhteys_pyyntö(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);data=bytearray()
                while b'\n' not in data and len(data)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    data.extend(조각)
                수신됨.append(('tcp',bytes(data)));자신.request.sendall(data)
        class datagrammi_kahva_pyyntö(socketserver.BaseRequestHandler):
            def handle(자신):
                data,vastake_ARVO=자신.request;수신됨.append(('udp',data));vastake_ARVO.sendto(data,자신.client_address)
        자신.yhteys_ohjain=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_portti),kahva_yhteys_pyyntö)
        try:자신.datagrammi_ohjain=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_portti),datagrammi_kahva_pyyntö)
        except Exception:자신.yhteys_ohjain.server_close();raise
        자신.yhteys_ohjain.daemon_threads=자신.datagrammi_ohjain.daemon_threads=True
        자신.TCP_portti=자신.yhteys_ohjain.server_address[1];자신.UDP_portti=자신.datagrammi_ohjain.server_address[1]

    def __enter__(자신):
        for palvelin_ARVO in (자신.yhteys_ohjain,자신.datagrammi_ohjain):
            työntekijä=threading.Thread(target=palvelin_ARVO.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            työntekijä.start();자신.작업가닥들.append(työntekijä)
        return 자신

    def __exit__(자신,*argumentti_MATRIISI):
        for palvelin_ARVO in (자신.yhteys_ohjain,자신.datagrammi_ohjain):palvelin_ARVO.shutdown();palvelin_ARVO.server_close()
        for työntekijä in 자신.작업가닥들:työntekijä.join(timeout=1)


if __name__=='__main__':
    jäsennin=argparse.ArgumentParser(description=__doc__)
    jäsennin.add_argument('--tcp-port',type=int,default=9000);jäsennin.add_argument('--udp-port',type=int,default=9001)
    argumentti_MATRIISI=jäsennin.parse_args()
    with päivitys_Palvelimet(argumentti_MATRIISI.tcp_port,argumentti_MATRIISI.udp_port) as päivitys_palvelin_merkintä:
        print('isäntä TCP {}, UDP {} Valmistele. 게스트 OSOITE: 10.0.2.2. Lopeta_ohjelma: Ctrl+C'.format(päivitys_palvelin_merkintä.TCP_portti,päivitys_palvelin_merkintä.UDP_portti),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
