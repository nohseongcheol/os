#!/usr/bin/env python3
"""Galego 네트워크 예제용 hospedar TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class eco_Servidores:
    def __init__(자신,TCP_porto=0,UDP_porto=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class agarradoira_conexión_solicitude(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);datos=bytearray()
                while b'\n' not in datos and len(datos)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    datos.extend(조각)
                수신됨.append(('tcp',bytes(datos)));자신.request.sendall(datos)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                datos,소켓=자신.request;수신됨.append(('udp',datos));소켓.sendto(datos,자신.client_address)
        자신.conexión_control=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_porto),agarradoira_conexión_solicitude)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_porto),전문요청처리)
        except Exception:자신.conexión_control.server_close();raise
        자신.conexión_control.daemon_threads=자신.전문제어.daemon_threads=True
        자신.TCP_porto=자신.conexión_control.server_address[1];자신.UDP_porto=자신.전문제어.server_address[1]

    def __enter__(자신):
        for servidor_VALOR in (자신.conexión_control,자신.전문제어):
            작업가닥=threading.Thread(target=servidor_VALOR.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*argumento_MATRIZ):
        for servidor_VALOR in (자신.conexión_control,자신.전문제어):servidor_VALOR.shutdown();servidor_VALOR.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    analizador=argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--tcp-port',type=int,default=9000);analizador.add_argument('--udp-port',type=int,default=9001)
    argumento_MATRIZ=analizador.parse_args()
    with eco_Servidores(argumento_MATRIZ.tcp_port,argumento_MATRIZ.udp_port) as eco_servidor_introdución:
        print('hospedar TCP {}, UDP {} 준비. 게스트 ENDEREZO: 10.0.2.2. saír_apl: Ctrl+C'.format(eco_servidor_introdución.TCP_porto,eco_servidor_introdución.UDP_porto),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
