#!/usr/bin/env python3
"""хост_рачунар 루프백 주소에만 바인딩하는 UDP 시험 сервер_вриједност. Ctrl+C로 종료한다."""
import argparse
import socket

def 실행():
    рашчлањивати_вриједност = argparse.ArgumentParser(description='jkoros корисник UDP 예제의 로컬 되돌림 сервер_вриједност')
    рашчлањивати_вриједност.add_argument('--port', type=int, default=9000)
    인자 = рашчлањивати_вриједност.parse_args()
    if not 1 <= 인자.port <= 65535: рашчлањивати_вриједност.error('порт_вриједност 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as сервер_вриједност:
        сервер_вриједност.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Припремити. Ctrl+C로 изаћи_програм.'.format(인자.port), flush=True)
        while True:
            подаци, peer_вриједност = сервер_вриједност.recvfrom(65535)
            сервер_вриједност.sendto(подаци, peer_вриједност)

if __name__ == '__main__':
    try: 실행()
    except KeyboardInterrupt: pass
