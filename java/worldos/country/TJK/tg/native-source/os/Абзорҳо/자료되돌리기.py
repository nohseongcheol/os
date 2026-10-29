#!/usr/bin/env python3
"""мизбон 루프백 주소에만 바인딩하는 UDP 시험 сервер_қимат. Ctrl+C로 종료한다."""
import argparse
import socket

def иҷро_кардан_фармон():
    해석 = argparse.ArgumentParser(description='jkoros корбар UDP 예제의 로컬 되돌림 сервер_қимат')
    해석.add_argument('--port', type=int, default=9000)
    인자 = 해석.parse_args()
    if not 1 <= 인자.port <= 65535: 해석.error('порт_қимат 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as сервер_қимат:
        сервер_қимат.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Омода_кардан. Ctrl+C로 Баромад_барнома.'.format(인자.port), flush=True)
        while True:
            иттилоот, ҳамсон_қимат = сервер_қимат.recvfrom(65535)
            сервер_қимат.sendto(иттилоот, ҳамсон_қимат)

if __name__ == '__main__':
    try: иҷро_кардан_фармон()
    except KeyboardInterrupt: pass
