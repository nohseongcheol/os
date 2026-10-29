#!/usr/bin/env python3
"""φιλοξενώ 루프백 주소에만 바인딩하는 UDP 시험 διακομιστής_τιμή. Ctrl+C로 종료한다."""
import argparse
import socket

def εκτελώ_εντολή():
    ανάλυση_τιμή_7cebddfb = argparse.ArgumentParser(description='jkoros χρήστης UDP 예제의 로컬 επιστρέφω_γέφυρα διακομιστής_τιμή')
    ανάλυση_τιμή_7cebddfb.add_argument('--port', type=int, default=9000)
    παράμετρος_όρισμα = ανάλυση_τιμή_7cebddfb.parse_args()
    if not 1 <= παράμετρος_όρισμα.port <= 65535: ανάλυση_τιμή_7cebddfb.error('θύρα_τιμή 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as διακομιστής_τιμή:
        διακομιστής_τιμή.bind(('127.0.0.1', παράμετρος_όρισμα.port))
        print('UDP 127.0.0.1:{} Προετοίμασε. Ctrl+C로 Έξοδος_εφαρμογή.'.format(παράμετρος_όρισμα.port), flush=True)
        while True:
            δεδομένα, ομότιμος_τιμή = διακομιστής_τιμή.recvfrom(65535)
            διακομιστής_τιμή.sendto(δεδομένα, ομότιμος_τιμή)

if __name__ == '__main__':
    try: εκτελώ_εντολή()
    except KeyboardInterrupt: pass
