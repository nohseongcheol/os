#!/usr/bin/env python3
"""ஓம்பு 루프백 주소에만 바인딩하는 UDP 시험 சேவையகம்_மதிப்பு. Ctrl+C로 종료한다."""
import argparse
import socket

def இயக்கு_கட்டளை():
    அலகிடு_மதிப்பு = argparse.ArgumentParser(description='jkoros பயனர் UDP 예제의 로컬 되돌림 சேவையகம்_மதிப்பு')
    அலகிடு_மதிப்பு.add_argument('--port', type=int, default=9000)
    அளவுரு_மதிப்புரு = அலகிடு_மதிப்பு.parse_args()
    if not 1 <= அளவுரு_மதிப்புரு.port <= 65535: அலகிடு_மதிப்பு.error('முணையம்_மதிப்பு 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as சேவையகம்_மதிப்பு:
        சேவையகம்_மதிப்பு.bind(('127.0.0.1', அளவுரு_மதிப்புரு.port))
        print('UDP 127.0.0.1:{} தயார்படுத்த. Ctrl+C로 முடிவு_நிரல்.'.format(அளவுரு_மதிப்புரு.port), flush=True)
        while True:
            தரவு, பியர்_மதிப்பு = சேவையகம்_மதிப்பு.recvfrom(65535)
            சேவையகம்_மதிப்பு.sendto(தரவு, பியர்_மதிப்பு)

if __name__ == '__main__':
    try: இயக்கு_கட்டளை()
    except KeyboardInterrupt: pass
