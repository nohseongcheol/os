#!/usr/bin/env python3
"""хост 루프백 주소에만 바인딩하는 UDP 시험 сервер_вриједност. Ctrl+C로 종료한다."""
import argparse
import socket

def Изврши_команда():
    рашчланити_вриједност = argparse.ArgumentParser(description='jkoros корисник UDP 예제의 로컬 вратити_мост сервер_вриједност')
    рашчланити_вриједност.add_argument('--port', type=int, default=9000)
    параметар_аргумент = рашчланити_вриједност.parse_args()
    if not 1 <= параметар_аргумент.port <= 65535: рашчланити_вриједност.error('порт_вриједност 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as сервер_вриједност:
        сервер_вриједност.bind(('127.0.0.1', параметар_аргумент.port))
        print('UDP 127.0.0.1:{} Припремити. Ctrl+C로 Излаз_програм.'.format(параметар_аргумент.port), flush=True)
        while True:
            подаци, 상대 = сервер_вриједност.recvfrom(65535)
            сервер_вриједност.sendto(подаци, 상대)

if __name__ == '__main__':
    try: Изврши_команда()
    except KeyboardInterrupt: pass
