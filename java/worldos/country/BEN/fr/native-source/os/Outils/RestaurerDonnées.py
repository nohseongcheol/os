#!/usr/bin/env python3
"""Hôte 루프백 주소에만 바인딩하는 UDP Tests valeurServeur. Ctrl+C로 종료한다."""
import argparse
import socket

def exécuterCommande():
    analyserValeur = argparse.ArgumentParser(description='jkoros Utilisateur UDP 예제의 로컬 pontRetourner valeurServeur')
    analyserValeur.add_argument('--port', type=int, default=9000)
    argumentParamètre = analyserValeur.parse_args()
    if not 1 <= argumentParamètre.port <= 65535: analyserValeur.error('valeurPort 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as valeurServeur:
        valeurServeur.bind(('127.0.0.1', argumentParamètre.port))
        print('UDP 127.0.0.1:{} préparer. Ctrl+C로 programmeQuitter.'.format(argumentParamètre.port), flush=True)
        while True:
            Données, valeurPairRéseau = valeurServeur.recvfrom(65535)
            valeurServeur.sendto(Données, valeurPairRéseau)

if __name__ == '__main__':
    try: exécuterCommande()
    except KeyboardInterrupt: pass
