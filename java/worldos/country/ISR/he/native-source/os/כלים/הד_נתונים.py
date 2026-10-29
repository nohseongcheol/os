#!/usr/bin/env python3
"""ארח 루프백 주소에만 바인딩하는 UDP 시험 שרת_ערך. Ctrl+C로 종료한다."""
import argparse
import socket

def לבצע_פקודה():
    ניתוח_מבנה_טקסט_ערך = argparse.ArgumentParser(description='jkoros משתמש UDP 예제의 로컬 החזר_גשר שרת_ערך')
    ניתוח_מבנה_טקסט_ערך.add_argument('--port', type=int, default=9000)
    פרמטר_ארגומנט = ניתוח_מבנה_טקסט_ערך.parse_args()
    if not 1 <= פרמטר_ארגומנט.port <= 65535: ניתוח_מבנה_טקסט_ערך.error('הסב_ערך 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as שרת_ערך:
        שרת_ערך.bind(('127.0.0.1', פרמטר_ארגומנט.port))
        print('UDP 127.0.0.1:{} להכין. Ctrl+C로 יציאה_תוכנית.'.format(פרמטר_ארגומנט.port), flush=True)
        while True:
            נתונים, עמית_ערך = שרת_ערך.recvfrom(65535)
            שרת_ערך.sendto(נתונים, עמית_ערך)

if __name__ == '__main__':
    try: לבצע_פקודה()
    except KeyboardInterrupt: pass
