#!/usr/bin/env python3
"""vert 루프백 주소에만 바인딩하는 UDP 시험 tenar_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def Utfør_kommando():
    dele_opp_VALUE = argparse.ArgumentParser(description='jkoros brukar UDP 예제의 로컬 levere_tilbake_bru tenar_VALUE')
    dele_opp_VALUE.add_argument('--port', type=int, default=9000)
    parameter_argument = dele_opp_VALUE.parse_args()
    if not 1 <= parameter_argument.port <= 65535: dele_opp_VALUE.error('port_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as tenar_VALUE:
        tenar_VALUE.bind(('127.0.0.1', parameter_argument.port))
        print('UDP 127.0.0.1:{} Klargjer. Ctrl+C로 Utgang_app.'.format(parameter_argument.port), flush=True)
        while True:
            data, node_VALUE_6a3b6fa7 = tenar_VALUE.recvfrom(65535)
            tenar_VALUE.sendto(data, node_VALUE_6a3b6fa7)

if __name__ == '__main__':
    try: Utfør_kommando()
    except KeyboardInterrupt: pass
