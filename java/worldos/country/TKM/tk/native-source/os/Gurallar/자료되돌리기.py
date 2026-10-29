#!/usr/bin/env python3
"""esasy 루프백 주소에만 바인딩하는 UDP 시험 serwer_baha. Ctrl+C로 종료한다."""
import argparse
import socket

def ýerine_ýetir_buýruk():
    seljer_baha = argparse.ArgumentParser(description='jkoros ulanyjy UDP 예제의 로컬 되돌림 serwer_baha')
    seljer_baha.add_argument('--port', type=int, default=9000)
    인자 = seljer_baha.parse_args()
    if not 1 <= 인자.port <= 65535: seljer_baha.error('port_baha 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as serwer_baha:
        serwer_baha.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Taýýarla. Ctrl+C로 çyk_programma.'.format(인자.port), flush=True)
        while True:
            maglumat, deň_derejeli_düwün_baha = serwer_baha.recvfrom(65535)
            serwer_baha.sendto(maglumat, deň_derejeli_düwün_baha)

if __name__ == '__main__':
    try: ýerine_ýetir_buýruk()
    except KeyboardInterrupt: pass
