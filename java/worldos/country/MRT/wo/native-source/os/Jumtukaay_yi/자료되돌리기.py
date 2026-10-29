#!/usr/bin/env python3
"""dalal 루프백 주소에만 바인딩하는 UDP 시험 dëggu_xëyma. Ctrl+C로 종료한다."""
import argparse
import socket

def def_ndigel():
    Segg_xëyma = argparse.ArgumentParser(description='jkoros kiy_jariñoo_internet UDP 예제의 로컬 되돌림 dëggu_xëyma')
    Segg_xëyma.add_argument('--port', type=int, default=9000)
    인자 = Segg_xëyma.parse_args()
    if not 1 <= 인자.port <= 65535: Segg_xëyma.error('jël_xëyma 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as dëggu_xëyma:
        dëggu_xëyma.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} jël_matuwaay. Ctrl+C로 Génn_jëfekaay.'.format(인자.port), flush=True)
        while True:
            mbir, Nàttangoo_xëyma = dëggu_xëyma.recvfrom(65535)
            dëggu_xëyma.sendto(mbir, Nàttangoo_xëyma)

if __name__ == '__main__':
    try: def_ndigel()
    except KeyboardInterrupt: pass
