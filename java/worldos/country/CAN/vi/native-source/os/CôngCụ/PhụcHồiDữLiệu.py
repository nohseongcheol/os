#!/usr/bin/env python3
"""Chủ 루프백 주소에만 바인딩하는 UDP KiểmThử giáTrịMáyChủ. Ctrl+C로 종료한다."""
import argparse
import socket

def thựcThiLệnh():
    phânTíchCúPhápGiáTrị = argparse.ArgumentParser(description='jkoros NgườiDùng UDP 예제의 로컬 cầuNốiTrảVề giáTrịMáyChủ')
    phânTíchCúPhápGiáTrị.add_argument('--port', type=int, default=9000)
    đốiSốThamSố = phânTíchCúPhápGiáTrị.parse_args()
    if not 1 <= đốiSốThamSố.port <= 65535: phânTíchCúPhápGiáTrị.error('giáTrịCổng 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as giáTrịMáyChủ:
        giáTrịMáyChủ.bind(('127.0.0.1', đốiSốThamSố.port))
        print('UDP 127.0.0.1:{} chuẩnBị. Ctrl+C로 chươngTrìnhRa.'.format(đốiSốThamSố.port), flush=True)
        while True:
            DữLiệu, giáTrịĐốiTác = giáTrịMáyChủ.recvfrom(65535)
            giáTrịMáyChủ.sendto(DữLiệu, giáTrịĐốiTác)

if __name__ == '__main__':
    try: thựcThiLệnh()
    except KeyboardInterrupt: pass
