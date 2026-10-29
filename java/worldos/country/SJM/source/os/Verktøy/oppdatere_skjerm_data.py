#!/usr/bin/env python3
"""vert 루프백 주소에만 바인딩하는 UDP 시험 server_VERDI. Ctrl+C로 종료한다."""
import argparse
import socket

def Utfør_kommando():
    dele_opp_VERDI = argparse.ArgumentParser(description='jkoros bruker UDP 예제의 로컬 return_bro server_VERDI')
    dele_opp_VERDI.add_argument('--port', type=int, default=9000)
    parameter_argument = dele_opp_VERDI.parse_args()
    if not 1 <= parameter_argument.port <= 65535: dele_opp_VERDI.error('port_VERDI 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_VERDI:
        server_VERDI.bind(('127.0.0.1', parameter_argument.port))
        print('UDP 127.0.0.1:{} Forbered. Ctrl+C로 Utgang_app.'.format(parameter_argument.port), flush=True)
        while True:
            data, node_VERDI_6a3b6fa7 = server_VERDI.recvfrom(65535)
            server_VERDI.sendto(data, node_VERDI_6a3b6fa7)

if __name__ == '__main__':
    try: Utfør_kommando()
    except KeyboardInterrupt: pass
