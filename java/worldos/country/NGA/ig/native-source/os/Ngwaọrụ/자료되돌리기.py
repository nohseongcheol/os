#!/usr/bin/env python3
"""usu 루프백 주소에만 바인딩하는 UDP 시험 savà_valuu. Ctrl+C로 종료한다."""
import argparse
import socket

def mee_nnyemiwu():
    kerìsịa_valuu = argparse.ArgumentParser(description='jkoros òjìàrụ UDP 예제의 로컬 되돌림 savà_valuu')
    kerìsịa_valuu.add_argument('--port', type=int, default=9000)
    인자 = kerìsịa_valuu.parse_args()
    if not 1 <= 인자.port <= 65535: kerìsịa_valuu.error('pọọt_valuu 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as savà_valuu:
        savà_valuu.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Kwado. Ctrl+C로 pụọ_app.'.format(인자.port), flush=True)
        while True:
            datà, ibè_valuu = savà_valuu.recvfrom(65535)
            savà_valuu.sendto(datà, ibè_valuu)

if __name__ == '__main__':
    try: mee_nnyemiwu()
    except KeyboardInterrupt: pass
