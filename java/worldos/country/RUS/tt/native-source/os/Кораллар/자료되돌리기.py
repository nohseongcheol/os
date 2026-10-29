#!/usr/bin/env python3
"""хост 루프백 주소에만 바인딩하는 UDP 시험 сервер_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def үтәргә_команда():
    бүлү_VALUE = argparse.ArgumentParser(description='jkoros кулланучы UDP 예제의 로컬 кайтару_күпер сервер_VALUE')
    бүлү_VALUE.add_argument('--port', type=int, default=9000)
    인자 = бүлү_VALUE.parse_args()
    if not 1 <= 인자.port <= 65535: бүлү_VALUE.error('порт_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as сервер_VALUE:
        сервер_VALUE.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Әзерләү. Ctrl+C로 Чыгу_кушымта.'.format(인자.port), flush=True)
        while True:
            мәгълүмат, тиңдәш_VALUE = сервер_VALUE.recvfrom(65535)
            сервер_VALUE.sendto(мәгълүмат, тиңдәш_VALUE)

if __name__ == '__main__':
    try: үтәргә_команда()
    except KeyboardInterrupt: pass
