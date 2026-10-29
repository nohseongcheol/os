#!/usr/bin/env python3
"""хост 루프백 주소에만 바인딩하는 UDP випробування сервер_значення. Ctrl+C로 종료한다."""
import argparse
import socket

def Виконати_команда():
    аналізувати_значення = argparse.ArgumentParser(description='jkoros простір_користувача UDP 예제의 로컬 повернути_міст сервер_значення')
    аналізувати_значення.add_argument('--port', type=int, default=9000)
    параметр_аргумент = аналізувати_значення.parse_args()
    if not 1 <= параметр_аргумент.port <= 65535: аналізувати_значення.error('порт_значення 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as сервер_значення:
        сервер_значення.bind(('127.0.0.1', параметр_аргумент.port))
        print('UDP 127.0.0.1:{} Готувати. Ctrl+C로 Вийти_програма.'.format(параметр_аргумент.port), flush=True)
        while True:
            дані, точка_значення = сервер_значення.recvfrom(65535)
            сервер_значення.sendto(дані, точка_значення)

if __name__ == '__main__':
    try: Виконати_команда()
    except KeyboardInterrupt: pass
