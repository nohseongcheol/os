#!/usr/bin/env python3
"""кабылдоо 루프백 주소에만 바인딩하는 UDP 시험 сервер_маани. Ctrl+C로 종료한다."""
import argparse
import socket

def аткаруу_буйрук():
    талдоо_маани = argparse.ArgumentParser(description='jkoros колдонуучу UDP 예제의 로컬 되돌림 сервер_маани')
    талдоо_маани.add_argument('--port', type=int, default=9000)
    인자 = талдоо_маани.parse_args()
    if not 1 <= 인자.port <= 65535: талдоо_маани.error('порт_маани 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as сервер_маани:
        сервер_маани.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Даярдоо. Ctrl+C로 Чыгуу_програм.'.format(인자.port), flush=True)
        while True:
            берилмелер, бирдей_маани = сервер_маани.recvfrom(65535)
            сервер_маани.sendto(берилмелер, бирдей_маани)

if __name__ == '__main__':
    try: аткаруу_буйрук()
    except KeyboardInterrupt: pass
