#!/usr/bin/env python3
"""go_nea_ditirelo 루프백 주소에만 바인딩하는 UDP 시험 seba_boleng. Ctrl+C로 종료한다."""
import argparse
import socket

def phethagatša_taelo():
    ripaganya_boleng = argparse.ArgumentParser(description='jkoros mošomiši UDP 예제의 로컬 되돌림 seba_boleng')
    ripaganya_boleng.add_argument('--port', type=int, default=9000)
    인자 = ripaganya_boleng.parse_args()
    if not 1 <= 인자.port <= 65535: ripaganya_boleng.error('phote_boleng 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as seba_boleng:
        seba_boleng.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Lokišetša. Ctrl+C로 Etšwa_tirišo.'.format(인자.port), flush=True)
        while True:
            data, sedirišwa_sa_legoro_le_tee_boleng = seba_boleng.recvfrom(65535)
            seba_boleng.sendto(data, sedirišwa_sa_legoro_le_tee_boleng)

if __name__ == '__main__':
    try: phethagatša_taelo()
    except KeyboardInterrupt: pass
