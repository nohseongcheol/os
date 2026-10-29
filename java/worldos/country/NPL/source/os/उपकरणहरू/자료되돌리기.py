#!/usr/bin/env python3
"""होस्ट 루프백 주소에만 바인딩하는 UDP 시험 सर्भर_मान. Ctrl+C로 종료한다."""
import argparse
import socket

def कार्यान्वयन_गर्नुहोस्_आदेश():
    पदच्छेद_गर्नुहोस्_मान = argparse.ArgumentParser(description='jkoros प्रयोगकर्ता UDP 예제의 로컬 되돌림 सर्भर_मान')
    पदच्छेद_गर्नुहोस्_मान.add_argument('--port', type=int, default=9000)
    인자 = पदच्छेद_गर्नुहोस्_मान.parse_args()
    if not 1 <= 인자.port <= 65535: पदच्छेद_गर्नुहोस्_मान.error('पोर्ट_मान 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as सर्भर_मान:
        सर्भर_मान.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} तयार_गर्नुहोस्. Ctrl+C로 बाहिर_जानुहोस्_अनुप्रयोग.'.format(인자.port), flush=True)
        while True:
            लगत, समान_मान = सर्भर_मान.recvfrom(65535)
            सर्भर_मान.sendto(लगत, समान_मान)

if __name__ == '__main__':
    try: कार्यान्वयन_गर्नुहोस्_आदेश()
    except KeyboardInterrupt: pass
