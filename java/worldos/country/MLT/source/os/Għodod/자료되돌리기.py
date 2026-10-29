#!/usr/bin/env python3
"""host 루프백 주소에만 바인딩하는 UDP 시험 server_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def eżegwixxa_kmand():
    analizza_VALUE = argparse.ArgumentParser(description='jkoros utent UDP 예제의 로컬 되돌림 server_VALUE')
    analizza_VALUE.add_argument('--port', type=int, default=9000)
    인자 = analizza_VALUE.parse_args()
    if not 1 <= 인자.port <= 65535: analizza_VALUE.error('port_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_VALUE:
        server_VALUE.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Ħejji. Ctrl+C로 Ħruġ_programm.'.format(인자.port), flush=True)
        while True:
            data, peer_VALUE = server_VALUE.recvfrom(65535)
            server_VALUE.sendto(data, peer_VALUE)

if __name__ == '__main__':
    try: eżegwixxa_kmand()
    except KeyboardInterrupt: pass
