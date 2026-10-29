#!/usr/bin/env python3
"""جێدەر 루프백 주소에만 바인딩하는 UDP 시험 ڕاژەکار_نرخ. Ctrl+C로 종료한다."""
import argparse
import socket

def جێبەجێکردن_فەرمان():
    해석 = argparse.ArgumentParser(description='jkoros بەکارهێنەر UDP 예제의 로컬 되돌림 ڕاژەکار_نرخ')
    해석.add_argument('--port', type=int, default=9000)
    인자 = 해석.parse_args()
    if not 1 <= 인자.port <= 65535: 해석.error('دەرگا_نرخ 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ڕاژەکار_نرخ:
        ڕاژەکار_نرخ.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} ئامادە_کردن_9ce364fc. Ctrl+C로 بزربوون_بەرنامە.'.format(인자.port), flush=True)
        while True:
            دەیتا, هاوتا_نرخ = ڕاژەکار_نرخ.recvfrom(65535)
            ڕاژەکار_نرخ.sendto(دەیتا, هاوتا_نرخ)

if __name__ == '__main__':
    try: جێبەجێکردن_فەرمان()
    except KeyboardInterrupt: pass
