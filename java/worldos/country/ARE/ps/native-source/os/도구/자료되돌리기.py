#!/usr/bin/env python3
"""کوربه 루프백 주소에만 바인딩하는 UDP 시험 서버. Ctrl+C로 종료한다."""
import argparse
import socket

def 실행():
    تجزیه_ارزښت = argparse.ArgumentParser(description='jkoros کارن UDP 예제의 로컬 되돌림 서버')
    تجزیه_ارزښت.add_argument('--port', type=int, default=9000)
    인자 = تجزیه_ارزښت.parse_args()
    if not 1 <= 인자.port <= 65535: تجزیه_ارزښت.error('درشل_ارزښت 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 서버:
        서버.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} 준비. Ctrl+C로 وتون_کاريال.'.format(인자.port), flush=True)
        while True:
            اومتوک, جوړه_ارزښت = 서버.recvfrom(65535)
            서버.sendto(اومتوک, جوړه_ارزښت)

if __name__ == '__main__':
    try: 실행()
    except KeyboardInterrupt: pass
