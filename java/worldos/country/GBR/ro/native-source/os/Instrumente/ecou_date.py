#!/usr/bin/env python3
"""gazdă 루프백 주소에만 바인딩하는 UDP 시험 server_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def executa_comandă():
    analiza_VALUE = argparse.ArgumentParser(description='jkoros utilizator UDP 예제의 로컬 restitui_punte server_VALUE')
    analiza_VALUE.add_argument('--port', type=int, default=9000)
    parametru_argument = analiza_VALUE.parse_args()
    if not 1 <= parametru_argument.port <= 65535: analiza_VALUE.error('muta_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_VALUE:
        server_VALUE.bind(('127.0.0.1', parametru_argument.port))
        print('UDP 127.0.0.1:{} Pregătiți. Ctrl+C로 ieși_program.'.format(parametru_argument.port), flush=True)
        while True:
            date, pereche_VALUE = server_VALUE.recvfrom(65535)
            server_VALUE.sendto(date, pereche_VALUE)

if __name__ == '__main__':
    try: executa_comandă()
    except KeyboardInterrupt: pass
