#!/usr/bin/env python3
"""organizuoti 루프백 주소에만 바인딩하는 UDP 시험 serveris_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def Vykdyti_komanda():
    analizuoti_sintaksę_VALUE = argparse.ArgumentParser(description='jkoros naudotojas UDP 예제의 로컬 grąžinti_tiltas serveris_VALUE')
    analizuoti_sintaksę_VALUE.add_argument('--port', type=int, default=9000)
    parametras_argumentas = analizuoti_sintaksę_VALUE.parse_args()
    if not 1 <= parametras_argumentas.port <= 65535: analizuoti_sintaksę_VALUE.error('jungtis_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as serveris_VALUE:
        serveris_VALUE.bind(('127.0.0.1', parametras_argumentas.port))
        print('UDP 127.0.0.1:{} Parengti. Ctrl+C로 Baigti_programa_086bb533.'.format(parametras_argumentas.port), flush=True)
        while True:
            duomenys, lygiavertis_mazgas_VALUE = serveris_VALUE.recvfrom(65535)
            serveris_VALUE.sendto(duomenys, lygiavertis_mazgas_VALUE)

if __name__ == '__main__':
    try: Vykdyti_komanda()
    except KeyboardInterrupt: pass
