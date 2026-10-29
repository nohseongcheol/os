#!/usr/bin/env python3
"""მასპინძელი 루프백 주소에만 바인딩하는 UDP 시험 სერვერი_მნიშვნელობა. Ctrl+C로 종료한다."""
import argparse
import socket

def შესრულება_ბრძანება():
    ანალიზი_მნიშვნელობა = argparse.ArgumentParser(description='jkoros მომხმარებელი UDP 예제의 로컬 დაბრუნება_ხიდი სერვერი_მნიშვნელობა')
    ანალიზი_მნიშვნელობა.add_argument('--port', type=int, default=9000)
    인자 = ანალიზი_მნიშვნელობა.parse_args()
    if not 1 <= 인자.port <= 65535: ანალიზი_მნიშვნელობა.error('პორტი_მნიშვნელობა 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as სერვერი_მნიშვნელობა:
        სერვერი_მნიშვნელობა.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} მომზადება. Ctrl+C로 გასვლა_აპი.'.format(인자.port), flush=True)
        while True:
            მონაცემები, კვანძი_მნიშვნელობა_6a3b6fa7 = სერვერი_მნიშვნელობა.recvfrom(65535)
            სერვერი_მნიშვნელობა.sendto(მონაცემები, კვანძი_მნიშვნელობა_6a3b6fa7)

if __name__ == '__main__':
    try: შესრულება_ბრძანება()
    except KeyboardInterrupt: pass
