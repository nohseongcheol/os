#!/usr/bin/env python3
"""tuttarvik 루프백 주소에만 바인딩하는 UDP 시험 ikiaqqitittivik_atuutilik. Ctrl+C로 종료한다."""
import argparse
import socket

def 실행():
    agguqtuut_atuutilik = argparse.ArgumentParser(description='jkoros atuqtuq UDP 예제의 로컬 되돌림 ikiaqqitittivik_atuutilik')
    agguqtuut_atuutilik.add_argument('--port', type=int, default=9000)
    인자 = agguqtuut_atuutilik.parse_args()
    if not 1 <= 인자.port <= 65535: agguqtuut_atuutilik.error('kapputigaq_atuutilik 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ikiaqqitittivik_atuutilik:
        ikiaqqitittivik_atuutilik.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Parnalli. Ctrl+C로 taima_pilirijjut.'.format(인자.port), flush=True)
        while True:
            titiqqat, ilagijaujuq_atuutilik = ikiaqqitittivik_atuutilik.recvfrom(65535)
            ikiaqqitittivik_atuutilik.sendto(titiqqat, ilagijaujuq_atuutilik)

if __name__ == '__main__':
    try: 실행()
    except KeyboardInterrupt: pass
