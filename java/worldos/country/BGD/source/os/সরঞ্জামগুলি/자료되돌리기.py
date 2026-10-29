#!/usr/bin/env python3
"""হোস্ট 루프백 주소에만 바인딩하는 UDP 시험 সার্ভার_মান. Ctrl+C로 종료한다."""
import argparse
import socket

def কার্যকর_করুন_আদেশ():
    বিভাজন_করা_মান = argparse.ArgumentParser(description='jkoros ব্যবহারকারী UDP 예제의 로컬 되돌림 সার্ভার_মান')
    বিভাজন_করা_মান.add_argument('--port', type=int, default=9000)
    প্যারামিটার_যুক্তি = বিভাজন_করা_মান.parse_args()
    if not 1 <= প্যারামিটার_যুক্তি.port <= 65535: বিভাজন_করা_মান.error('পোর্ট_মান 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as সার্ভার_মান:
        সার্ভার_মান.bind(('127.0.0.1', প্যারামিটার_যুক্তি.port))
        print('UDP 127.0.0.1:{} প্রস্তুত_করুন. Ctrl+C로 প্রস্থান_অ্যাপ.'.format(প্যারামিটার_যুক্তি.port), flush=True)
        while True:
            ডাটা, পিয়ার_মান = সার্ভার_মান.recvfrom(65535)
            সার্ভার_মান.sendto(ডাটা, পিয়ার_মান)

if __name__ == '__main__':
    try: কার্যকর_করুন_আদেশ()
    except KeyboardInterrupt: pass
