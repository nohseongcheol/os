#!/usr/bin/env python3
"""hostit 루프백 주소에만 바인딩하는 UDP zkoušky server_HODNOTA. Ctrl+C로 종료한다."""
import argparse
import socket

def Provést_příkaz():
    parsovat_HODNOTA = argparse.ArgumentParser(description='jkoros uživatelský_prostor UDP 예제의 로컬 Vratka_most server_HODNOTA')
    parsovat_HODNOTA.add_argument('--port', type=int, default=9000)
    parametr_argument = parsovat_HODNOTA.parse_args()
    if not 1 <= parametr_argument.port <= 65535: parsovat_HODNOTA.error('port_HODNOTA 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_HODNOTA:
        server_HODNOTA.bind(('127.0.0.1', parametr_argument.port))
        print('UDP 127.0.0.1:{} Připravit. Ctrl+C로 Konec_program.'.format(parametr_argument.port), flush=True)
        while True:
            data, partner_HODNOTA = server_HODNOTA.recvfrom(65535)
            server_HODNOTA.sendto(data, partner_HODNOTA)

if __name__ == '__main__':
    try: Provést_příkaz()
    except KeyboardInterrupt: pass
