#!/usr/bin/env python3
"""ਹੋਸਟ 루프백 주소에만 바인딩하는 UDP 시험 ਸਰਵਰ_ਕੀਮਤ. Ctrl+C로 종료한다."""
import argparse
import socket

def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼():
    ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ = argparse.ArgumentParser(description='jkoros ਉਪਭੋਗਤਾ UDP 예제의 로컬 되돌림 ਸਰਵਰ_ਕੀਮਤ')
    ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.add_argument('--port', type=int, default=9000)
    인자 = ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.parse_args()
    if not 1 <= 인자.port <= 65535: ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.error('ਪੋਰਟ_ਕੀਮਤ 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ਸਰਵਰ_ਕੀਮਤ:
        ਸਰਵਰ_ਕੀਮਤ.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} ਤਿਆਰ_ਕਰੋ. Ctrl+C로 ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼.'.format(인자.port), flush=True)
        while True:
            ਸਮੱਗਰੀ, ਪਿਅਰ_ਕੀਮਤ = ਸਰਵਰ_ਕੀਮਤ.recvfrom(65535)
            ਸਰਵਰ_ਕੀਮਤ.sendto(ਸਮੱਗਰੀ, ਪਿਅਰ_ਕੀਮਤ)

if __name__ == '__main__':
    try: ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
    except KeyboardInterrupt: pass
