#!/usr/bin/env python3
"""taurima 루프백 주소에만 바인딩하는 UDP 시험 tūmau_uara. Ctrl+C로 종료한다."""
import argparse
import socket

def kawe_tono():
    poroporo_uara = argparse.ArgumentParser(description='jkoros kaiwhakamahi UDP 예제의 로컬 되돌림 tūmau_uara')
    poroporo_uara.add_argument('--port', type=int, default=9000)
    인자 = poroporo_uara.parse_args()
    if not 1 <= 인자.port <= 65535: poroporo_uara.error('kawe_uara 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as tūmau_uara:
        tūmau_uara.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Whakarite. Ctrl+C로 Putaatu_kaupapa.'.format(인자.port), flush=True)
        while True:
            raraunga, hoa_uara = tūmau_uara.recvfrom(65535)
            tūmau_uara.sendto(raraunga, hoa_uara)

if __name__ == '__main__':
    try: kawe_tono()
    except KeyboardInterrupt: pass
