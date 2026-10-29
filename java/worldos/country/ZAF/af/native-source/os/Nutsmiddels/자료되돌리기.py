#!/usr/bin/env python3
"""hou 루프백 주소에만 바인딩하는 UDP 시험 bediener_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def uitvoer_bevel():
    ontleed_VALUE = argparse.ArgumentParser(description='jkoros gebruiker UDP 예제의 로컬 teruggee_brug bediener_VALUE')
    ontleed_VALUE.add_argument('--port', type=int, default=9000)
    인자 = ontleed_VALUE.parse_args()
    if not 1 <= 인자.port <= 65535: ontleed_VALUE.error('ombou_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as bediener_VALUE:
        bediener_VALUE.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Maak_gereed. Ctrl+C로 Verlaat_program.'.format(인자.port), flush=True)
        while True:
            data, portuur_VALUE = bediener_VALUE.recvfrom(65535)
            bediener_VALUE.sendto(data, portuur_VALUE)

if __name__ == '__main__':
    try: uitvoer_bevel()
    except KeyboardInterrupt: pass
