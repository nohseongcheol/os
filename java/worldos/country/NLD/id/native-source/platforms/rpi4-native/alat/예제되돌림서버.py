#!/usr/bin/env python3
"""Indonesia 네트워크 예제용 host TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class echo_Server:
    def __init__(자신,TCP_port=0,UDP_port=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class handel_koneksi_permintaan(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);data=bytearray()
                while b'\n' not in data and len(data)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    data.extend(조각)
                수신됨.append(('tcp',bytes(data)));자신.request.sendall(data)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                data,소켓=자신.request;수신됨.append(('udp',data));소켓.sendto(data,자신.client_address)
        자신.koneksi_kontrol=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_port),handel_koneksi_permintaan)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_port),전문요청처리)
        except Exception:자신.koneksi_kontrol.server_close();raise
        자신.koneksi_kontrol.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_port=자신.koneksi_kontrol.server_address[1];자신.UDP_port=자신.전문제어.server_address[1]

    def __enter__(자신):
        for server_VALUE in (자신.koneksi_kontrol,자신.전문제어):
            tugasLatar=threading.Thread(target=server_VALUE.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            tugasLatar.start();자신.작업가닥들.append(tugasLatar)
        return 자신

    def __exit__(자신,*argumen_ARRAY):
        for server_VALUE in (자신.koneksi_kontrol,자신.전문제어):server_VALUE.shutdown();server_VALUE.server_close()
        for tugasLatar in 자신.작업가닥들:tugasLatar.join(timeout=1)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tcp-port',type=int,default=9000);parser.add_argument('--udp-port',type=int,default=9001)
    argumen_ARRAY=parser.parse_args()
    with echo_Server(argumen_ARRAY.tcp_port,argumen_ARRAY.udp_port) as echo_server_entri:
        print('host TCP {}, UDP {} Siapkan. 게스트 surel: 10.0.2.2. Keluar_apl: Ctrl+C'.format(echo_server_entri.TCP_port,echo_server_entri.UDP_port),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
