#!/usr/bin/env python3
"""вдоми 루프백 주소에만 바인딩하는 UDP 시험 сервер_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def Изврши_наредба():
    разложи_VALUE = argparse.ArgumentParser(description='jkoros корисник UDP 예제의 로컬 되돌림 сервер_VALUE')
    разложи_VALUE.add_argument('--port', type=int, default=9000)
    параметар_аргумент = разложи_VALUE.parse_args()
    if not 1 <= параметар_аргумент.port <= 65535: разложи_VALUE.error('порта_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as сервер_VALUE:
        сервер_VALUE.bind(('127.0.0.1', параметар_аргумент.port))
        print('UDP 127.0.0.1:{} Подготви. Ctrl+C로 Излез_програма.'.format(параметар_аргумент.port), flush=True)
        while True:
            податоци, рамноправен_уред_VALUE = сервер_VALUE.recvfrom(65535)
            сервер_VALUE.sendto(податоци, рамноправен_уред_VALUE)

if __name__ == '__main__':
    try: Изврши_наредба()
    except KeyboardInterrupt: pass
