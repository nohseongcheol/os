#!/usr/bin/env python3
"""gucumbikira 루프백 주소에만 바인딩하는 UDP 시험 seriveri_agaciro. Ctrl+C로 종료한다."""
import argparse
import socket

def gukora_ibwiriza():
    gusesengura_agaciro = argparse.ArgumentParser(description='jkoros ukoresha UDP 예제의 로컬 되돌림 seriveri_agaciro')
    gusesengura_agaciro.add_argument('--port', type=int, default=9000)
    인자 = gusesengura_agaciro.parse_args()
    if not 1 <= 인자.port <= 65535: gusesengura_agaciro.error('poti_agaciro 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as seriveri_agaciro:
        seriveri_agaciro.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Gutegura. Ctrl+C로 gusohoka_porogaramu.'.format(인자.port), flush=True)
        while True:
            amakurushingiro, Mugenzi_agaciro = seriveri_agaciro.recvfrom(65535)
            seriveri_agaciro.sendto(amakurushingiro, Mugenzi_agaciro)

if __name__ == '__main__':
    try: gukora_ibwiriza()
    except KeyboardInterrupt: pass
