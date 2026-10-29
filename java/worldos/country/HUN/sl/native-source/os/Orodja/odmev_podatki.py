#!/usr/bin/env python3
"""gostiti 루프백 주소에만 바인딩하는 UDP 시험 strežnik_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def Izvedi_ukaz():
    razčlenjevati_VALUE = argparse.ArgumentParser(description='jkoros uporabnik UDP 예제의 로컬 vrni_most strežnik_VALUE')
    razčlenjevati_VALUE.add_argument('--port', type=int, default=9000)
    parameter_argument = razčlenjevati_VALUE.parse_args()
    if not 1 <= parameter_argument.port <= 65535: razčlenjevati_VALUE.error('vrata_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as strežnik_VALUE:
        strežnik_VALUE.bind(('127.0.0.1', parameter_argument.port))
        print('UDP 127.0.0.1:{} Pripravi. Ctrl+C로 Izhod_aplikacija.'.format(parameter_argument.port), flush=True)
        while True:
            podatki, enakovreden_VALUE = strežnik_VALUE.recvfrom(65535)
            strežnik_VALUE.sendto(podatki, enakovreden_VALUE)

if __name__ == '__main__':
    try: Izvedi_ukaz()
    except KeyboardInterrupt: pass
