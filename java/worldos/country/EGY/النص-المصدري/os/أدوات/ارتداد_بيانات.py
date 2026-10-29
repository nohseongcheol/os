#!/usr/bin/env python3
"""مضيف 루프백 주소에만 바인딩하는 UDP اختبارات خادم_قيمة. Ctrl+C로 종료한다."""
import argparse
import socket

def ينفذ_أمر():
    يوزّع_قيمة = argparse.ArgumentParser(description='jkoros فضاء_المستخدم UDP 예제의 로컬 إرجاع_جسر خادم_قيمة')
    يوزّع_قيمة.add_argument('--port', type=int, default=9000)
    معلمة_وسيطة = يوزّع_قيمة.parse_args()
    if not 1 <= معلمة_وسيطة.port <= 65535: يوزّع_قيمة.error('منفذ_قيمة 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as خادم_قيمة:
        خادم_قيمة.bind(('127.0.0.1', معلمة_وسيطة.port))
        print('UDP 127.0.0.1:{} إعداد. Ctrl+C로 خروج_تطبيق.'.format(معلمة_وسيطة.port), flush=True)
        while True:
            بيانات, نظير_قيمة = خادم_قيمة.recvfrom(65535)
            خادم_قيمة.sendto(بيانات, نظير_قيمة)

if __name__ == '__main__':
    try: ينفذ_أمر()
    except KeyboardInterrupt: pass
