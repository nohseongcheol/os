#!/usr/bin/env python3
"""pinagare 루프백 주소에만 바인딩하는 UDP 시험 sefara_Boleng. Ctrl+C로 종료한다."""
import argparse
import socket

def diragatsa_Taelo():
    go_lokolola_Boleng = argparse.ArgumentParser(description='jkoros modirisi UDP 예제의 로컬 되돌림 sefara_Boleng')
    go_lokolola_Boleng.add_argument('--port', type=int, default=9000)
    인자 = go_lokolola_Boleng.parse_args()
    if not 1 <= 인자.port <= 65535: go_lokolola_Boleng.error('gorogisetsa_Boleng 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sefara_Boleng:
        sefara_Boleng.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Baakanya. Ctrl+C로 tswaya_Tiriso.'.format(인자.port), flush=True)
        while True:
            tshedimosetso, semphato_Boleng = sefara_Boleng.recvfrom(65535)
            sefara_Boleng.sendto(tshedimosetso, semphato_Boleng)

if __name__ == '__main__':
    try: diragatsa_Taelo()
    except KeyboardInterrupt: pass
