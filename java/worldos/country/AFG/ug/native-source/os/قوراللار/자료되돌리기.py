#!/usr/bin/env python3
"""باقار 루프백 주소에만 바인딩하는 UDP 시험 مۇلازىمىتېر_قىممىتى. Ctrl+C로 종료한다."""
import argparse
import socket

def ئىجرا_قىلىش_بۇيرۇق():
    해석 = argparse.ArgumentParser(description='jkoros ئىشلەتكۈچى UDP 예제의 로컬 قايتۇرۇپ_بېرىش_كۆۋرۈك مۇلازىمىتېر_قىممىتى')
    해석.add_argument('--port', type=int, default=9000)
    인자 = 해석.parse_args()
    if not 1 <= 인자.port <= 65535: 해석.error('ئېغىز_قىممىتى 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as مۇلازىمىتېر_قىممىتى:
        مۇلازىمىتېر_قىممىتى.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} تەييارلىماق. Ctrl+C로 چىقىش_ئەپ.'.format(인자.port), flush=True)
        while True:
            مەلۇمات, باراۋەرلىك_قىممىتى = مۇلازىمىتېر_قىممىتى.recvfrom(65535)
            مۇلازىمىتېر_قىممىتى.sendto(مەلۇمات, باراۋەرلىك_قىممىتى)

if __name__ == '__main__':
    try: ئىجرا_قىلىش_بۇيرۇق()
    except KeyboardInterrupt: pass
