#!/usr/bin/env python3
"""singatha 루프백 주소에만 바인딩하는 UDP 시험 Iseva_inani. Ctrl+C로 종료한다."""
import argparse
import socket

def yenza_umyalo():
    zawula_inani = argparse.ArgumentParser(description='jkoros umsebenzisi UDP 예제의 로컬 되돌림 Iseva_inani')
    zawula_inani.add_argument('--port', type=int, default=9000)
    인자 = zawula_inani.parse_args()
    if not 1 <= 인자.port <= 65535: zawula_inani.error('intuba_inani 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as Iseva_inani:
        Iseva_inani.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Hlela. Ctrl+C로 phuma_i_app.'.format(인자.port), flush=True)
        while True:
            imininingwane, untanga_inani = Iseva_inani.recvfrom(65535)
            Iseva_inani.sendto(imininingwane, untanga_inani)

if __name__ == '__main__':
    try: yenza_umyalo()
    except KeyboardInterrupt: pass
