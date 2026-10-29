#!/usr/bin/env python3
"""میزبان 루프백 주소에만 바인딩하는 UDP 시험 سرور_قدر. Ctrl+C로 종료한다."""
import argparse
import socket

def نفاذ_کریں_حکم():
    پارس_قدر = argparse.ArgumentParser(description='jkoros صارف UDP 예제의 로컬 되돌림 سرور_قدر')
    پارس_قدر.add_argument('--port', type=int, default=9000)
    پیرا_میٹر_دلائل = پارس_قدر.parse_args()
    if not 1 <= پیرا_میٹر_دلائل.port <= 65535: پارس_قدر.error('پورٹ_قدر 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as سرور_قدر:
        سرور_قدر.bind(('127.0.0.1', پیرا_میٹر_دلائل.port))
        print('UDP 127.0.0.1:{} تیار_کریں. Ctrl+C로 خروج_ایپ.'.format(پیرا_میٹر_دلائل.port), flush=True)
        while True:
            کوائف, ساتھی_قدر = سرور_قدر.recvfrom(65535)
            سرور_قدر.sendto(کوائف, ساتھی_قدر)

if __name__ == '__main__':
    try: نفاذ_کریں_حکم()
    except KeyboardInterrupt: pass
