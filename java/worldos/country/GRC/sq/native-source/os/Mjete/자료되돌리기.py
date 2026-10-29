#!/usr/bin/env python3
"""pritës 루프백 주소에만 바인딩하는 UDP 시험 server_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def zbatoj_komandë():
    analizoj_VALUE = argparse.ArgumentParser(description='jkoros përdorues UDP 예제의 로컬 Kthe_urë server_VALUE')
    analizoj_VALUE.add_argument('--port', type=int, default=9000)
    parametër_argument = analizoj_VALUE.parse_args()
    if not 1 <= parametër_argument.port <= 65535: analizoj_VALUE.error('portë_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_VALUE:
        server_VALUE.bind(('127.0.0.1', parametër_argument.port))
        print('UDP 127.0.0.1:{} Përgatit. Ctrl+C로 dal_program.'.format(parametër_argument.port), flush=True)
        while True:
            të_dhëna, homolog_VALUE = server_VALUE.recvfrom(65535)
            server_VALUE.sendto(të_dhëna, homolog_VALUE)

if __name__ == '__main__':
    try: zbatoj_komandë()
    except KeyboardInterrupt: pass
