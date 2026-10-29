#!/usr/bin/env python3
"""hostiteľ 루프백 주소에만 바인딩하는 UDP 시험 server_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def Vykonať_príkaz():
    analyzovať_VALUE = argparse.ArgumentParser(description='jkoros používateľ UDP 예제의 로컬 vrátiť_most server_VALUE')
    analyzovať_VALUE.add_argument('--port', type=int, default=9000)
    parameter_argument = analyzovať_VALUE.parse_args()
    if not 1 <= parameter_argument.port <= 65535: analyzovať_VALUE.error('port_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_VALUE:
        server_VALUE.bind(('127.0.0.1', parameter_argument.port))
        print('UDP 127.0.0.1:{} Pripraviť. Ctrl+C로 Skončiť_program.'.format(parameter_argument.port), flush=True)
        while True:
            údaje, partnerský_uzol_VALUE = server_VALUE.recvfrom(65535)
            server_VALUE.sendto(údaje, partnerský_uzol_VALUE)

if __name__ == '__main__':
    try: Vykonať_príkaz()
    except KeyboardInterrupt: pass
