#!/usr/bin/env python3
"""ଆୟୋଜକ 루프백 주소에만 바인딩하는 UDP 시험 ସର୍ଭର୍_ମୂଲ୍ୟ. Ctrl+C로 종료한다."""
import argparse
import socket

def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ():
    ପାର୍ସ_ମୂଲ୍ୟ = argparse.ArgumentParser(description='jkoros ଉପଭୋକ୍ତା UDP 예제의 로컬 되돌림 ସର୍ଭର୍_ମୂଲ୍ୟ')
    ପାର୍ସ_ମୂଲ୍ୟ.add_argument('--port', type=int, default=9000)
    ପାରାମିଟର୍_ଯୁକ୍ତି = ପାର୍ସ_ମୂଲ୍ୟ.parse_args()
    if not 1 <= ପାରାମିଟର୍_ଯୁକ୍ତି.port <= 65535: ପାର୍ସ_ମୂଲ୍ୟ.error('ପୋର୍ଟ_ମୂଲ୍ୟ 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ସର୍ଭର୍_ମୂଲ୍ୟ:
        ସର୍ଭର୍_ମୂଲ୍ୟ.bind(('127.0.0.1', ପାରାମିଟର୍_ଯୁକ୍ତି.port))
        print('UDP 127.0.0.1:{} ପ୍ରସ୍ତୁତ. Ctrl+C로 ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ.'.format(ପାରାମିଟର୍_ଯୁକ୍ତି.port), flush=True)
        while True:
            ଡାଟା, ସମକକ୍ଷ_ମୂଲ୍ୟ = ସର୍ଭର୍_ମୂଲ୍ୟ.recvfrom(65535)
            ସର୍ଭର୍_ମୂଲ୍ୟ.sendto(ଡାଟା, ସମକକ୍ଷ_ମୂଲ୍ୟ)

if __name__ == '__main__':
    try: ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
    except KeyboardInterrupt: pass
