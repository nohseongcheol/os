#!/usr/bin/env python3
"""ධාරකය 루프백 주소에만 바인딩하는 UDP 시험 සේවාදායකය_අගය. Ctrl+C로 종료한다."""
import argparse
import socket

def ක්_රියාත්මක_කරන්න_විධානය():
    විශ්ලේෂණය_කරන්න_අගය = argparse.ArgumentParser(description='jkoros පරිශීලක UDP 예제의 로컬 되돌림 සේවාදායකය_අගය')
    විශ්ලේෂණය_කරන්න_අගය.add_argument('--port', type=int, default=9000)
    인자 = විශ්ලේෂණය_කරන්න_අගය.parse_args()
    if not 1 <= 인자.port <= 65535: විශ්ලේෂණය_කරන්න_අගය.error('තොට_අගය 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as සේවාදායකය_අගය:
        සේවාදායකය_අගය.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} පිළියෙල_කරන්න. Ctrl+C로 පිටවීම_යෙදු.'.format(인자.port), flush=True)
        while True:
            දත්ත, සමානයා_අගය = සේවාදායකය_අගය.recvfrom(65535)
            සේවාදායකය_අගය.sendto(දත්ත, සමානයා_අගය)

if __name__ == '__main__':
    try: ක්_රියාත්මක_කරන්න_විධානය()
    except KeyboardInterrupt: pass
