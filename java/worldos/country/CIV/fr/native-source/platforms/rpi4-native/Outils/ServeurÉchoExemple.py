#!/usr/bin/env python3
"""français 네트워크 예제용 Hôte TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class ServeursRépercuter:
    def __init__(valeurSoi,portTCP=0,portUDP=0):
        valeurSoi.possèdeReçu=[];valeurSoi.filsExécution=[]
        possèdeReçu=valeurSoi.possèdeReçu
        class requêteConnexionPoignée(socketserver.BaseRequestHandler):
            def handle(valeurSoi):
                valeurSoi.request.settimeout(5);Données=bytearray()
                while b'\n' not in Données and len(Données)<=512:
                    valeurFragment=valeurSoi.request.recv(512)
                    if not valeurFragment:return
                    Données.extend(valeurFragment)
                possèdeReçu.append(('tcp',bytes(Données)));valeurSoi.request.sendall(Données)
        class requêtePoignéeDatagramme(socketserver.BaseRequestHandler):
            def handle(valeurSoi):
                Données,valeurPriseRéseau=valeurSoi.request;possèdeReçu.append(('udp',Données));valeurPriseRéseau.sendto(Données,valeurSoi.client_address)
        valeurSoi.contrôleConnexion=socketserver.ThreadingTCPServer(('127.0.0.1',portTCP),requêteConnexionPoignée)
        try:valeurSoi.contrôleDatagramme=socketserver.ThreadingUDPServer(('127.0.0.1',portUDP),requêtePoignéeDatagramme)
        except Exception:valeurSoi.contrôleConnexion.server_close();raise
        valeurSoi.contrôleConnexion.daemon_threads=valeurSoi.contrôleDatagramme.daemon_threads=True
        valeurSoi.portTCP=valeurSoi.contrôleConnexion.server_address[1];valeurSoi.portUDP=valeurSoi.contrôleDatagramme.server_address[1]

    def __enter__(valeurSoi):
        for valeurServeur in (valeurSoi.contrôleConnexion,valeurSoi.contrôleDatagramme):
            tâcheFond=threading.Thread(target=valeurServeur.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            tâcheFond.start();valeurSoi.filsExécution.append(tâcheFond)
        return valeurSoi

    def __exit__(valeurSoi,*tableauArgument):
        for valeurServeur in (valeurSoi.contrôleConnexion,valeurSoi.contrôleDatagramme):valeurServeur.shutdown();valeurServeur.server_close()
        for tâcheFond in valeurSoi.filsExécution:tâcheFond.join(timeout=1)


if __name__=='__main__':
    analyseur=argparse.ArgumentParser(description=__doc__)
    analyseur.add_argument('--tcp-port',type=int,default=9000);analyseur.add_argument('--udp-port',type=int,default=9001)
    tableauArgument=analyseur.parse_args()
    with ServeursRépercuter(tableauArgument.tcp_port,tableauArgument.udp_port) as entréeÉlémentServeurRépercuter:
        print('Hôte TCP {}, UDP {} préparer. 게스트 adresse: 10.0.2.2. programmeQuitter: Ctrl+C'.format(entréeÉlémentServeurRépercuter.portTCP,entréeÉlémentServeurRépercuter.portUDP),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
