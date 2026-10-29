#!/usr/bin/env python3
"""орналастыру 루프백 주소에만 바인딩하는 UDP 시험 сервер_мән. Ctrl+C로 종료한다."""
import argparse
import socket

def орындау_пәрмен():
    талдау_мән = argparse.ArgumentParser(description='jkoros пайдаланушы UDP 예제의 로컬 қайтару_көпір сервер_мән')
    талдау_мән.add_argument('--port', type=int, default=9000)
    параметр_аргумент = талдау_мән.parse_args()
    if not 1 <= параметр_аргумент.port <= 65535: талдау_мән.error('порт_мән 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as сервер_мән:
        сервер_мән.bind(('127.0.0.1', параметр_аргумент.port))
        print('UDP 127.0.0.1:{} Дайындау. Ctrl+C로 Шығу_бағдарлама.'.format(параметр_аргумент.port), flush=True)
        while True:
            деректер, бір_рангілі_мән = сервер_мән.recvfrom(65535)
            сервер_мән.sendto(деректер, бір_рангілі_мән)

if __name__ == '__main__':
    try: орындау_пәрмен()
    except KeyboardInterrupt: pass
