#!/usr/bin/env python3
"""viesot 루프백 주소에만 바인딩하는 UDP 시험 serveris_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def Izpildīt_komanda():
    parsēt_VALUE = argparse.ArgumentParser(description='jkoros lietotājs UDP 예제의 로컬 atdot_tilts serveris_VALUE')
    parsēt_VALUE.add_argument('--port', type=int, default=9000)
    parametrs_arg = parsēt_VALUE.parse_args()
    if not 1 <= parametrs_arg.port <= 65535: parsēt_VALUE.error('ports_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as serveris_VALUE:
        serveris_VALUE.bind(('127.0.0.1', parametrs_arg.port))
        print('UDP 127.0.0.1:{} Sagatavot. Ctrl+C로 Iziet_programma.'.format(parametrs_arg.port), flush=True)
        while True:
            dati, vienranga_VALUE = serveris_VALUE.recvfrom(65535)
            serveris_VALUE.sendto(dati, vienranga_VALUE)

if __name__ == '__main__':
    try: Izpildīt_komanda()
    except KeyboardInterrupt: pass
