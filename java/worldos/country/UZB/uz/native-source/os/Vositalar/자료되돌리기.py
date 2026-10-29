#!/usr/bin/env python3
"""tashkilotchi 루프백 주소에만 바인딩하는 UDP 시험 server_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def bajarmoq_buyruq():
    tahlil_qilmoq_VALUE = argparse.ArgumentParser(description='jkoros foydalanuvchi UDP 예제의 로컬 되돌림 server_VALUE')
    tahlil_qilmoq_VALUE.add_argument('--port', type=int, default=9000)
    인자 = tahlil_qilmoq_VALUE.parse_args()
    if not 1 <= 인자.port <= 65535: tahlil_qilmoq_VALUE.error('port_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_VALUE:
        server_VALUE.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Tayyorlamoq. Ctrl+C로 Chiqish_ilova.'.format(인자.port), flush=True)
        while True:
            ma_lumotlar, bir_rangli_VALUE = server_VALUE.recvfrom(65535)
            server_VALUE.sendto(ma_lumotlar, bir_rangli_VALUE)

if __name__ == '__main__':
    try: bajarmoq_buyruq()
    except KeyboardInterrupt: pass
