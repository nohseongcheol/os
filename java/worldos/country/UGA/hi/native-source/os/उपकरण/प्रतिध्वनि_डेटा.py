#!/usr/bin/env python3
"""आयोजक 루프백 주소에만 바인딩하는 UDP 시험 서버. Ctrl+C로 종료한다."""
import argparse
import socket

def निष्पादित_करें_आदेश():
    पार्स_करें_मान = argparse.ArgumentParser(description='jkoros उपयोगकर्ता UDP 예제의 로컬 वापस_करें_ब्रिज 서버')
    पार्स_करें_मान.add_argument('--port', type=int, default=9000)
    पैरामीटर_तर्क = पार्स_करें_मान.parse_args()
    if not 1 <= पैरामीटर_तर्क.port <= 65535: पार्स_करें_मान.error('पोर्ट_मान 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 서버:
        서버.bind(('127.0.0.1', पैरामीटर_तर्क.port))
        print('UDP 127.0.0.1:{} 준비. Ctrl+C로 निर्गमन_ऐप.'.format(पैरामीटर_तर्क.port), flush=True)
        while True:
            आँकड़े, पीअर_मान = 서버.recvfrom(65535)
            서버.sendto(आँकड़े, पीअर_मान)

if __name__ == '__main__':
    try: निष्पादित_करें_आदेश()
    except KeyboardInterrupt: pass
