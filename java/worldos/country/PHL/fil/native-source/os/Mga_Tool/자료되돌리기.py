#!/usr/bin/env python3
"""host 루프백 주소에만 바인딩하는 UDP 시험 server_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def Mag_execute_utos():
    mag_parse_VALUE = argparse.ArgumentParser(description='jkoros gumagamit UDP 예제의 로컬 되돌림 server_VALUE')
    mag_parse_VALUE.add_argument('--port', type=int, default=9000)
    parameter_argumento = mag_parse_VALUE.parse_args()
    if not 1 <= parameter_argumento.port <= 65535: mag_parse_VALUE.error('port_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_VALUE:
        server_VALUE.bind(('127.0.0.1', parameter_argumento.port))
        print('UDP 127.0.0.1:{} Ihanda. Ctrl+C로 Paglabas_app.'.format(parameter_argumento.port), flush=True)
        while True:
            data, peer_VALUE = server_VALUE.recvfrom(65535)
            server_VALUE.sendto(data, peer_VALUE)

if __name__ == '__main__':
    try: Mag_execute_utos()
    except KeyboardInterrupt: pass
