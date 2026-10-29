#!/usr/bin/env python3
"""óstach 루프백 주소에만 바인딩하는 UDP 시험 freastalaí_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def Rith_ordú():
    parsáil_VALUE = argparse.ArgumentParser(description='jkoros úsáideoir UDP 예제의 로컬 return_traschóiritheoir freastalaí_VALUE')
    parsáil_VALUE.add_argument('--port', type=int, default=9000)
    paraiméadar_argóint = parsáil_VALUE.parse_args()
    if not 1 <= paraiméadar_argóint.port <= 65535: parsáil_VALUE.error('port_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as freastalaí_VALUE:
        freastalaí_VALUE.bind(('127.0.0.1', paraiméadar_argóint.port))
        print('UDP 127.0.0.1:{} Ullmhaigh. Ctrl+C로 scoir_clár.'.format(paraiméadar_argóint.port), flush=True)
        while True:
            sonraí, piara_VALUE = freastalaí_VALUE.recvfrom(65535)
            freastalaí_VALUE.sendto(sonraí, piara_VALUE)

if __name__ == '__main__':
    try: Rith_ordú()
    except KeyboardInterrupt: pass
