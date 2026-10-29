#!/usr/bin/env python3
"""Português 네트워크 예제용 host TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class eco_Servidores:
    def __init__(자신,porta_TCP=0,UDP_porta=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class alça_conexão_solicitação(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);dados=bytearray()
                while b'\n' not in dados and len(dados)<=512:
                    fragmento_VALOR=자신.request.recv(512)
                    if not fragmento_VALOR:return
                    dados.extend(fragmento_VALOR)
                수신됨.append(('tcp',bytes(dados)));자신.request.sendall(dados)
        class datagrama_alça_solicitação(socketserver.BaseRequestHandler):
            def handle(자신):
                dados,soquete_VALOR=자신.request;수신됨.append(('udp',dados));soquete_VALOR.sendto(dados,자신.client_address)
        자신.conexão_visual=socketserver.ThreadingTCPServer(('127.0.0.1',porta_TCP),alça_conexão_solicitação)
        try:자신.datagrama_visual=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_porta),datagrama_alça_solicitação)
        except Exception:자신.conexão_visual.server_close();raise
        자신.conexão_visual.daemon_threads=자신.datagrama_visual.daemon_threads=True
        자신.porta_TCP=자신.conexão_visual.server_address[1];자신.UDP_porta=자신.datagrama_visual.server_address[1]

    def __enter__(자신):
        for servidor_VALOR in (자신.conexão_visual,자신.datagrama_visual):
            tarefaSegundoPlano=threading.Thread(target=servidor_VALOR.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            tarefaSegundoPlano.start();자신.작업가닥들.append(tarefaSegundoPlano)
        return 자신

    def __exit__(자신,*argumento_MATRIZ):
        for servidor_VALOR in (자신.conexão_visual,자신.datagrama_visual):servidor_VALOR.shutdown();servidor_VALOR.server_close()
        for tarefaSegundoPlano in 자신.작업가닥들:tarefaSegundoPlano.join(timeout=1)


if __name__=='__main__':
    analisador=argparse.ArgumentParser(description=__doc__)
    analisador.add_argument('--tcp-port',type=int,default=9000);analisador.add_argument('--udp-port',type=int,default=9001)
    argumento_MATRIZ=analisador.parse_args()
    with eco_Servidores(argumento_MATRIZ.tcp_port,argumento_MATRIZ.udp_port) as eco_servidor_entrada:
        print('host TCP {}, UDP {} Preparar. 게스트 Endereço: 10.0.2.2. sair_app: Ctrl+C'.format(eco_servidor_entrada.porta_TCP,eco_servidor_entrada.UDP_porta),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
