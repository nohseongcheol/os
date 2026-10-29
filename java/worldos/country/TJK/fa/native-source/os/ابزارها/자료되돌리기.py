#!/usr/bin/env python3
"""میزبان 루프백 주소에만 바인딩하는 UDP 시험 سرور_مقدار. Ctrl+C로 종료한다."""
import argparse
import socket

def اجرا_فرمان():
    تفسیر_مقدار = argparse.ArgumentParser(description='jkoros کاربر UDP 예제의 로컬 بازگرداندن_پل سرور_مقدار')
    تفسیر_مقدار.add_argument('--port', type=int, default=9000)
    پارامتر_آرگومان = تفسیر_مقدار.parse_args()
    if not 1 <= پارامتر_آرگومان.port <= 65535: تفسیر_مقدار.error('تبدیل_مقدار 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as سرور_مقدار:
        سرور_مقدار.bind(('127.0.0.1', پارامتر_آرگومان.port))
        print('UDP 127.0.0.1:{} آماده_کردن. Ctrl+C로 خروج_برنامه.'.format(پارامتر_آرگومان.port), flush=True)
        while True:
            داده_ها, مشابه_مقدار = سرور_مقدار.recvfrom(65535)
            سرور_مقدار.sendto(داده_ها, مشابه_مقدار)

if __name__ == '__main__':
    try: اجرا_فرمان()
    except KeyboardInterrupt: pass
