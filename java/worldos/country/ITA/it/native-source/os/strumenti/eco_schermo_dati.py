#!/usr/bin/env python3
"""host 루프백 주소에만 바인딩하는 UDP prove server_VALORE. Ctrl+C로 종료한다."""
import argparse
import socket

def Esegui_comando():
    analizzare_VALORE = argparse.ArgumentParser(description='jkoros spazio_utente UDP 예제의 로컬 Reso_bridge server_VALORE')
    analizzare_VALORE.add_argument('--port', type=int, default=9000)
    parametro_argomento = analizzare_VALORE.parse_args()
    if not 1 <= parametro_argomento.port <= 65535: analizzare_VALORE.error('porta_VALORE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_VALORE:
        server_VALORE.bind(('127.0.0.1', parametro_argomento.port))
        print('UDP 127.0.0.1:{} Prepara. Ctrl+C로 Esci_app.'.format(parametro_argomento.port), flush=True)
        while True:
            dati, peer_VALORE = server_VALORE.recvfrom(65535)
            server_VALORE.sendto(dati, peer_VALORE)

if __name__ == '__main__':
    try: Esegui_comando()
    except KeyboardInterrupt: pass
