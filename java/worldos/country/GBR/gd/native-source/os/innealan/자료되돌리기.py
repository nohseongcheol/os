#!/usr/bin/env python3
"""òstair 루프백 주소에만 바인딩하는 UDP 시험 frithealaiche_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def gnìomhaich_àithne():
    해석 = argparse.ArgumentParser(description='jkoros cleachdaiche UDP 예제의 로컬 return_drochaid frithealaiche_VALUE')
    해석.add_argument('--port', type=int, default=9000)
    인자 = 해석.parse_args()
    if not 1 <= 인자.port <= 65535: 해석.error('port_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as frithealaiche_VALUE:
        frithealaiche_VALUE.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Ullaich. Ctrl+C로 fàg_ap.'.format(인자.port), flush=True)
        while True:
            dàta, seise_VALUE = frithealaiche_VALUE.recvfrom(65535)
            frithealaiche_VALUE.sendto(dàta, seise_VALUE)

if __name__ == '__main__':
    try: gnìomhaich_àithne()
    except KeyboardInterrupt: pass
