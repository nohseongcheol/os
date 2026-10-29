#!/usr/bin/env python3
"""مہمان_b78e430d 루프백 주소에만 바인딩하는 UDP 시험 سرور_قدر. Ctrl+C로 종료한다."""
import argparse
import socket

def نفاذ_کرو_حکم():
    해석 = argparse.ArgumentParser(description='jkoros صارف UDP 예제의 로컬 되돌림 سرور_قدر')
    해석.add_argument('--port', type=int, default=9000)
    인자 = 해석.parse_args()
    if not 1 <= 인자.port <= 65535: 해석.error('دہانہ_قدر 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as سرور_قدر:
        سرور_قدر.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} تیاری_کرو. Ctrl+C로 خارج_کرو_ایپ.'.format(인자.port), flush=True)
        while True:
            کوائف, ہم_سر_قدر = سرور_قدر.recvfrom(65535)
            سرور_قدر.sendto(کوائف, ہم_سر_قدر)

if __name__ == '__main__':
    try: نفاذ_کرو_حکم()
    except KeyboardInterrupt: pass
