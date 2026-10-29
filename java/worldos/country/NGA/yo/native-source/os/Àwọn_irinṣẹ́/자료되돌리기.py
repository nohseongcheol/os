#!/usr/bin/env python3
"""olùpèsè 루프백 주소에만 바인딩하는 UDP 시험 apèsè_iye. Ctrl+C로 종료한다."""
import argparse
import socket

def ṣiṣẹ́_àṣẹ():
    ìpínsíwẹ́wẹ́_iye = argparse.ArgumentParser(description='jkoros aṣàmúlò UDP 예제의 로컬 되돌림 apèsè_iye')
    ìpínsíwẹ́wẹ́_iye.add_argument('--port', type=int, default=9000)
    인자 = ìpínsíwẹ́wẹ́_iye.parse_args()
    if not 1 <= 인자.port <= 65535: ìpínsíwẹ́wẹ́_iye.error('ojú_iye 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as apèsè_iye:
        apèsè_iye.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} gbaradì. Ctrl+C로 jáde_àtòjọ_ètò.'.format(인자.port), flush=True)
        while True:
            détà, ọ̀gbà_iye = apèsè_iye.recvfrom(65535)
            apèsè_iye.sendto(détà, ọ̀gbà_iye)

if __name__ == '__main__':
    try: ṣiṣẹ́_àṣẹ()
    except KeyboardInterrupt: pass
