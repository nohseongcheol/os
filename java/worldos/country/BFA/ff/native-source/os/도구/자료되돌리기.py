#!/usr/bin/env python3
"""njaatigi 루프백 주소에만 바인딩하는 UDP 시험 sarworde_njaru. Ctrl+C로 종료한다."""
import argparse
import socket

def 실행():
    해석 = argparse.ArgumentParser(description='jkoros kuutoro UDP 예제의 로컬 되돌림 sarworde_njaru')
    해석.add_argument('--port', type=int, default=9000)
    인자 = 해석.parse_args()
    if not 1 <= 인자.port <= 65535: 해석.error('poor_njaru 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sarworde_njaru:
        sarworde_njaru.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Heblu. Ctrl+C로 yaltude_tafirde.'.format(인자.port), flush=True)
        while True:
            keɓe, giƴiraaɗo_njaru = sarworde_njaru.recvfrom(65535)
            sarworde_njaru.sendto(keɓe, giƴiraaɗo_njaru)

if __name__ == '__main__':
    try: 실행()
    except KeyboardInterrupt: pass
