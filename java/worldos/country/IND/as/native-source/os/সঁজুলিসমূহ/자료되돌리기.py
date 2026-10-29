#!/usr/bin/env python3
"""হ_ষ্ট 루프백 주소에만 바인딩하는 UDP 시험 ছাৰ্ভাৰ_মান. Ctrl+C로 종료한다."""
import argparse
import socket

def নিষ্পাদন_আদেশ():
    পাৰ্ছ_কৰক_মান = argparse.ArgumentParser(description='jkoros ব্যৱহাৰকৰ্তা UDP 예제의 로컬 되돌림 ছাৰ্ভাৰ_মান')
    পাৰ্ছ_কৰক_মান.add_argument('--port', type=int, default=9000)
    인자 = পাৰ্ছ_কৰক_মান.parse_args()
    if not 1 <= 인자.port <= 65535: পাৰ্ছ_কৰক_মান.error('পৰ্ট_মান 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ছাৰ্ভাৰ_মান:
        ছাৰ্ভাৰ_মান.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} প্ৰস্তুত_কৰক. Ctrl+C로 প্ৰস্থান_এপ্প্.'.format(인자.port), flush=True)
        while True:
            ডাটা, পীয়েৰ_মান = ছাৰ্ভাৰ_মান.recvfrom(65535)
            ছাৰ্ভাৰ_মান.sendto(ডাটা, পীয়েৰ_মান)

if __name__ == '__main__':
    try: নিষ্পাদন_আদেশ()
    except KeyboardInterrupt: pass
