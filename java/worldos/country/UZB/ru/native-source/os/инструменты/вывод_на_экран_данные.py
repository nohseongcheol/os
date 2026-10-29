#!/usr/bin/env python3
"""узел 루프백 주소에만 바인딩하는 UDP испытания сервер_ЗНАЧЕН. Ctrl+C로 종료한다."""
import argparse
import socket

def 실행():
    анализировать_ЗНАЧЕН = argparse.ArgumentParser(description='jkoros пространство_пользователя UDP 예제의 로컬 Возврат_мост сервер_ЗНАЧЕН')
    анализировать_ЗНАЧЕН.add_argument('--port', type=int, default=9000)
    параметр_аргумент = анализировать_ЗНАЧЕН.parse_args()
    if not 1 <= параметр_аргумент.port <= 65535: анализировать_ЗНАЧЕН.error('порт_ЗНАЧЕН 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as сервер_ЗНАЧЕН:
        сервер_ЗНАЧЕН.bind(('127.0.0.1', параметр_аргумент.port))
        print('UDP 127.0.0.1:{} Подготовить. Ctrl+C로 Выход_программа.'.format(параметр_аргумент.port), flush=True)
        while True:
            данные, одноранговый_ЗНАЧЕН = сервер_ЗНАЧЕН.recvfrom(65535)
            сервер_ЗНАЧЕН.sendto(данные, одноранговый_ЗНАЧЕН)

if __name__ == '__main__':
    try: 실행()
    except KeyboardInterrupt: pass
