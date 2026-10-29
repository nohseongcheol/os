#!/usr/bin/env python3
"""host 루프백 주소에만 바인딩하는 UDP tests server_WAARDE. Ctrl+C로 종료한다."""
import argparse
import socket

def Uitvoeren_opdracht():
    parseren_WAARDE = argparse.ArgumentParser(description='jkoros gebruikersruimte UDP 예제의 로컬 Retour_brug server_WAARDE')
    parseren_WAARDE.add_argument('--port', type=int, default=9000)
    parameter_argument = parseren_WAARDE.parse_args()
    if not 1 <= parameter_argument.port <= 65535: parseren_WAARDE.error('poort_WAARDE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_WAARDE:
        server_WAARDE.bind(('127.0.0.1', parameter_argument.port))
        print('UDP 127.0.0.1:{} Bereid_voor. Ctrl+C로 Einde_app.'.format(parameter_argument.port), flush=True)
        while True:
            gegevens, peer_WAARDE = server_WAARDE.recvfrom(65535)
            server_WAARDE.sendto(gegevens, peer_WAARDE)

if __name__ == '__main__':
    try: Uitvoeren_opdracht()
    except KeyboardInterrupt: pass
