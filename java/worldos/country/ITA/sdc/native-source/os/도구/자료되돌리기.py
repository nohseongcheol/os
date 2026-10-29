#!/usr/bin/env python3
"""호스트 루프백 주소에만 바인딩하는 UDP 시험 서버. Ctrl+C로 종료한다."""
import argparse
import socket

def 실행():
    해석 = argparse.ArgumentParser(description='jkoros 사용자 UDP 예제의 로컬 되돌림 서버')
    해석.add_argument('--port', type=int, default=9000)
    인자 = 해석.parse_args()
    if not 1 <= 인자.port <= 65535: 해석.error('창구 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 서버:
        서버.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} 준비. Ctrl+C로 종료.'.format(인자.port), flush=True)
        while True:
            자료, 상대 = 서버.recvfrom(65535)
            서버.sendto(자료, 상대)

if __name__ == '__main__':
    try: 실행()
    except KeyboardInterrupt: pass
