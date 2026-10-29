#!/usr/bin/env python3
"""Host 루프백 주소에만 바인딩하는 UDP 시험 Server_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def ausféieren_Befeel():
    analyséieren_VALUE = argparse.ArgumentParser(description='jkoros Benotzer UDP 예제의 로컬 되돌림 Server_VALUE')
    analyséieren_VALUE.add_argument('--port', type=int, default=9000)
    인자 = analyséieren_VALUE.parse_args()
    if not 1 <= 인자.port <= 65535: analyséieren_VALUE.error('Port_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as Server_VALUE:
        Server_VALUE.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Préparéieren. Ctrl+C로 Schluss_App.'.format(인자.port), flush=True)
        while True:
            Daten, Peer_VALUE = Server_VALUE.recvfrom(65535)
            Server_VALUE.sendto(Daten, Peer_VALUE)

if __name__ == '__main__':
    try: ausféieren_Befeel()
    except KeyboardInterrupt: pass
