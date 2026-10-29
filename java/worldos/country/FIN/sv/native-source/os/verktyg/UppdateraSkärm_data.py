#!/usr/bin/env python3
"""värd 루프백 주소에만 바인딩하는 UDP tester server_värde. Ctrl+C로 종료한다."""
import argparse
import socket

def köra_kommando():
    parsa_värde = argparse.ArgumentParser(description='jkoros användarutrymme UDP 예제의 로컬 Retur_brygga server_värde')
    parsa_värde.add_argument('--port', type=int, default=9000)
    parameter_argument = parsa_värde.parse_args()
    if not 1 <= parameter_argument.port <= 65535: parsa_värde.error('port_värde 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_värde:
        server_värde.bind(('127.0.0.1', parameter_argument.port))
        print('UDP 127.0.0.1:{} Förbereda. Ctrl+C로 Utgång_app.'.format(parameter_argument.port), flush=True)
        while True:
            data, peer_värde = server_värde.recvfrom(65535)
            server_värde.sendto(data, peer_värde)

if __name__ == '__main__':
    try: köra_kommando()
    except KeyboardInterrupt: pass
