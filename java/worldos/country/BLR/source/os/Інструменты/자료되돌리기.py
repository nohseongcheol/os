#!/usr/bin/env python3
"""вузел 루프백 주소에만 바인딩하는 UDP 시험 сервер_значэнне. Ctrl+C로 종료한다."""
import argparse
import socket

def выканаць_каманда():
    해석 = argparse.ArgumentParser(description='jkoros карыстальнік UDP 예제의 로컬 되돌림 сервер_значэнне')
    해석.add_argument('--port', type=int, default=9000)
    параметр_аргумент = 해석.parse_args()
    if not 1 <= параметр_аргумент.port <= 65535: 해석.error('порт_значэнне 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as сервер_значэнне:
        сервер_значэнне.bind(('127.0.0.1', параметр_аргумент.port))
        print('UDP 127.0.0.1:{} Падрыхтаваць. Ctrl+C로 Выхад_праграма.'.format(параметр_аргумент.port), flush=True)
        while True:
            дадзеныя, аднарангавы_значэнне = сервер_значэнне.recvfrom(65535)
            сервер_значэнне.sendto(дадзеныя, аднарангавы_значэнне)

if __name__ == '__main__':
    try: выканаць_каманда()
    except KeyboardInterrupt: pass
