#!/usr/bin/env python3
"""host 루프백 주소에만 바인딩하는 UDP 시험 server_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def Izvrši_komanda():
    raščlaniti_VALUE = argparse.ArgumentParser(description='jkoros korisnik UDP 예제의 로컬 vratiti_most server_VALUE')
    raščlaniti_VALUE.add_argument('--port', type=int, default=9000)
    parametar_argument = raščlaniti_VALUE.parse_args()
    if not 1 <= parametar_argument.port <= 65535: raščlaniti_VALUE.error('port_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_VALUE:
        server_VALUE.bind(('127.0.0.1', parametar_argument.port))
        print('UDP 127.0.0.1:{} Pripremi. Ctrl+C로 Izađi_program.'.format(parametar_argument.port), flush=True)
        while True:
            podaci, ravnopravni_uređaj_VALUE = server_VALUE.recvfrom(65535)
            server_VALUE.sendto(podaci, ravnopravni_uređaj_VALUE)

if __name__ == '__main__':
    try: Izvrši_komanda()
    except KeyboardInterrupt: pass
