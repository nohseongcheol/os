#!/usr/bin/env python3
"""հոստ 루프백 주소에만 바인딩하는 UDP 시험 սպասարկիչ_արժեք. Ctrl+C로 종료한다."""
import argparse
import socket

def կատարել_հրաման():
    վերլուծել_արժեք = argparse.ArgumentParser(description='jkoros օգտվող UDP 예제의 로컬 վերադարձնել_կամուրջ սպասարկիչ_արժեք')
    վերլուծել_արժեք.add_argument('--port', type=int, default=9000)
    인자 = վերլուծել_արժեք.parse_args()
    if not 1 <= 인자.port <= 65535: վերլուծել_արժեք.error('միացք_արժեք 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as սպասարկիչ_արժեք:
        սպասարկիչ_արժեք.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Պատրաստել. Ctrl+C로 Ելք_ծրագիր.'.format(인자.port), flush=True)
        while True:
            տվյալ, հավասարազոր_սարք_արժեք = սպասարկիչ_արժեք.recvfrom(65535)
            սպասարկիչ_արժեք.sendto(տվյալ, հավասարազոր_սարք_արժեք)

if __name__ == '__main__':
    try: կատարել_հրաման()
    except KeyboardInterrupt: pass
