#!/usr/bin/env python3
"""хост 루프백 주소에만 바인딩하는 UDP 시험 сървър_стойност. Ctrl+C로 종료한다."""
import argparse
import socket

def изпълнявам_команда():
    анализирам_стойност = argparse.ArgumentParser(description='jkoros потребител UDP 예제의 로컬 връщам_мост сървър_стойност')
    анализирам_стойност.add_argument('--port', type=int, default=9000)
    параметър_аргумент = анализирам_стойност.parse_args()
    if not 1 <= параметър_аргумент.port <= 65535: анализирам_стойност.error('порт_стойност 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as сървър_стойност:
        сървър_стойност.bind(('127.0.0.1', параметър_аргумент.port))
        print('UDP 127.0.0.1:{} Подготвяне. Ctrl+C로 Изход_програма.'.format(параметър_аргумент.port), flush=True)
        while True:
            данни, крайно_устройство_стойност = сървър_стойност.recvfrom(65535)
            сървър_стойност.sendto(данни, крайно_устройство_стойност)

if __name__ == '__main__':
    try: изпълнявам_команда()
    except KeyboardInterrupt: pass
