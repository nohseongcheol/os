#!/usr/bin/env python3
"""hýsa 루프백 주소에만 바인딩하는 UDP 시험 þjónn_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def keyra_skipun():
    þátta_VALUE = argparse.ArgumentParser(description='jkoros notandi UDP 예제의 로컬 skila_brú þjónn_VALUE')
    þátta_VALUE.add_argument('--port', type=int, default=9000)
    færibreyta_frumbreyta = þátta_VALUE.parse_args()
    if not 1 <= færibreyta_frumbreyta.port <= 65535: þátta_VALUE.error('gátt_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as þjónn_VALUE:
        þjónn_VALUE.bind(('127.0.0.1', færibreyta_frumbreyta.port))
        print('UDP 127.0.0.1:{} Undirbúa. Ctrl+C로 loka_forrit.'.format(færibreyta_frumbreyta.port), flush=True)
        while True:
            gögn, jafningi_VALUE = þjónn_VALUE.recvfrom(65535)
            þjónn_VALUE.sendto(gögn, jafningi_VALUE)

if __name__ == '__main__':
    try: keyra_skipun()
    except KeyboardInterrupt: pass
