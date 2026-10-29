#!/usr/bin/env python3
"""español 네트워크 예제용 Anfitrión TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class ServidoresRepetirEntrada:
    def __init__(valorPropio,puertoTCP=0,puertoUDP=0):
        valorPropio.tieneRecibido=[];valorPropio.hilosEjecución=[]
        tieneRecibido=valorPropio.tieneRecibido
        class peticiónConexiónManejador(socketserver.BaseRequestHandler):
            def handle(valorPropio):
                valorPropio.request.settimeout(5);Datos=bytearray()
                while b'\n' not in Datos and len(Datos)<=512:
                    valorFragmento=valorPropio.request.recv(512)
                    if not valorFragmento:return
                    Datos.extend(valorFragmento)
                tieneRecibido.append(('tcp',bytes(Datos)));valorPropio.request.sendall(Datos)
        class peticiónManejadorDatagrama(socketserver.BaseRequestHandler):
            def handle(valorPropio):
                Datos,valorConectorRed=valorPropio.request;tieneRecibido.append(('udp',Datos));valorConectorRed.sendto(Datos,valorPropio.client_address)
        valorPropio.controlConexión=socketserver.ThreadingTCPServer(('127.0.0.1',puertoTCP),peticiónConexiónManejador)
        try:valorPropio.controlDatagrama=socketserver.ThreadingUDPServer(('127.0.0.1',puertoUDP),peticiónManejadorDatagrama)
        except Exception:valorPropio.controlConexión.server_close();raise
        valorPropio.controlConexión.daemon_threads=valorPropio.controlDatagrama.daemon_threads=True
        valorPropio.puertoTCP=valorPropio.controlConexión.server_address[1];valorPropio.puertoUDP=valorPropio.controlDatagrama.server_address[1]

    def __enter__(valorPropio):
        for valorServidor in (valorPropio.controlConexión,valorPropio.controlDatagrama):
            tareaFondo=threading.Thread(target=valorServidor.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            tareaFondo.start();valorPropio.hilosEjecución.append(tareaFondo)
        return valorPropio

    def __exit__(valorPropio,*arregloArgumento):
        for valorServidor in (valorPropio.controlConexión,valorPropio.controlDatagrama):valorServidor.shutdown();valorServidor.server_close()
        for tareaFondo in valorPropio.hilosEjecución:tareaFondo.join(timeout=1)


if __name__=='__main__':
    analizador=argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--tcp-port',type=int,default=9000);analizador.add_argument('--udp-port',type=int,default=9001)
    arregloArgumento=analizador.parse_args()
    with ServidoresRepetirEntrada(arregloArgumento.tcp_port,arregloArgumento.udp_port) as entradaElementoServidorRepetirEntrada:
        print('Anfitrión TCP {}, UDP {} preparar. 게스트 dirección: 10.0.2.2. programaSalir: Ctrl+C'.format(entradaElementoServidorRepetirEntrada.puertoTCP,entradaElementoServidorRepetirEntrada.puertoUDP),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
