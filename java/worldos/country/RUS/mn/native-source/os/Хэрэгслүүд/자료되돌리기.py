#!/usr/bin/env python3
"""хост 루프백 주소에만 바인딩하는 UDP 시험 сервер_утга. Ctrl+C로 종료한다."""
import argparse
import socket

def Гүйцэтгэх_команд():
    задлан_ялгал_хийх_утга = argparse.ArgumentParser(description='jkoros хэрэглэгч UDP 예제의 로컬 되돌림 сервер_утга')
    задлан_ялгал_хийх_утга.add_argument('--port', type=int, default=9000)
    인자 = задлан_ялгал_хийх_утга.parse_args()
    if not 1 <= 인자.port <= 65535: задлан_ялгал_хийх_утга.error('порт_утга 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as сервер_утга:
        сервер_утга.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Бэлтгэх. Ctrl+C로 Гарах_програм.'.format(인자.port), flush=True)
        while True:
            өгөгдөл, ижил_түвшин_утга = сервер_утга.recvfrom(65535)
            сервер_утга.sendto(өгөгдөл, ижил_түвшин_утга)

if __name__ == '__main__':
    try: Гүйцэтгэх_команд()
    except KeyboardInterrupt: pass
