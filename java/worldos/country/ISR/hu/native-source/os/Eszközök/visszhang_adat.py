#!/usr/bin/env python3
"""gazda 루프백 주소에만 바인딩하는 UDP 시험 kiszolgáló_ÉRTÉK. Ctrl+C로 종료한다."""
import argparse
import socket

def végrehajt_parancs():
    elemez_ÉRTÉK = argparse.ArgumentParser(description='jkoros felhasználó UDP 예제의 로컬 visszaküld_híd kiszolgáló_ÉRTÉK')
    elemez_ÉRTÉK.add_argument('--port', type=int, default=9000)
    paraméter_argumentum = elemez_ÉRTÉK.parse_args()
    if not 1 <= paraméter_argumentum.port <= 65535: elemez_ÉRTÉK.error('port_ÉRTÉK 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as kiszolgáló_ÉRTÉK:
        kiszolgáló_ÉRTÉK.bind(('127.0.0.1', paraméter_argumentum.port))
        print('UDP 127.0.0.1:{} Előkészítés. Ctrl+C로 kilép_app.'.format(paraméter_argumentum.port), flush=True)
        while True:
            adat, társ_ÉRTÉK = kiszolgáló_ÉRTÉK.recvfrom(65535)
            kiszolgáló_ÉRTÉK.sendto(adat, társ_ÉRTÉK)

if __name__ == '__main__':
    try: végrehajt_parancs()
    except KeyboardInterrupt: pass
