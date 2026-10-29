#!/usr/bin/env python3
"""Català 네트워크 예제용 allotjar TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class eco_Servidors:
    def __init__(자신,TCP_port=0,UDP_port=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class control_connexió_sol_licitud(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);dades=bytearray()
                while b'\n' not in dades and len(dades)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    dades.extend(조각)
                수신됨.append(('tcp',bytes(dades)));자신.request.sendall(dades)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                dades,소켓=자신.request;수신됨.append(('udp',dades));소켓.sendto(dades,자신.client_address)
        자신.connexió_control=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_port),control_connexió_sol_licitud)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_port),전문요청처리)
        except Exception:자신.connexió_control.server_close();raise
        자신.connexió_control.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_port=자신.connexió_control.server_address[1];자신.UDP_port=자신.전문제어.server_address[1]

    def __enter__(자신):
        for servidor_VALOR in (자신.connexió_control,자신.전문제어):
            작업가닥=threading.Thread(target=servidor_VALOR.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*arg_MATRIU):
        for servidor_VALOR in (자신.connexió_control,자신.전문제어):servidor_VALOR.shutdown();servidor_VALOR.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    analitzador=argparse.ArgumentParser(description=__doc__)
    analitzador.add_argument('--tcp-port',type=int,default=9000);analitzador.add_argument('--udp-port',type=int,default=9001)
    arg_MATRIU=analitzador.parse_args()
    with eco_Servidors(arg_MATRIU.tcp_port,arg_MATRIU.udp_port) as eco_servidor_introducció:
        print('allotjar TCP {}, UDP {} Prepara. 게스트 Adreça: 10.0.2.2. Surt_programa: Ctrl+C'.format(eco_servidor_introducció.TCP_port,eco_servidor_introducció.UDP_port),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
