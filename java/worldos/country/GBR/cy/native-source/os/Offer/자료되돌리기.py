#!/usr/bin/env python3
"""lletya 루프백 주소에만 바인딩하는 UDP 시험 gweinydd_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def Gweithredu_gorchymyn():
    dosrannu_VALUE = argparse.ArgumentParser(description='jkoros defnyddiwr UDP 예제의 로컬 return_pont gweinydd_VALUE')
    dosrannu_VALUE.add_argument('--port', type=int, default=9000)
    paramedr_arg = dosrannu_VALUE.parse_args()
    if not 1 <= paramedr_arg.port <= 65535: dosrannu_VALUE.error('porth_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as gweinydd_VALUE:
        gweinydd_VALUE.bind(('127.0.0.1', paramedr_arg.port))
        print('UDP 127.0.0.1:{} Paratoi. Ctrl+C로 gadael_Rhaglen.'.format(paramedr_arg.port), flush=True)
        while True:
            data, cymar_VALUE = gweinydd_VALUE.recvfrom(65535)
            gweinydd_VALUE.sendto(data, cymar_VALUE)

if __name__ == '__main__':
    try: Gweithredu_gorchymyn()
    except KeyboardInterrupt: pass
