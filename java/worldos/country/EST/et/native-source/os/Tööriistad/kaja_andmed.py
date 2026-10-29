#!/usr/bin/env python3
"""host 루프백 주소에만 바인딩하는 UDP 시험 server_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def Täida_käsk():
    sõeluma_VALUE = argparse.ArgumentParser(description='jkoros kasutaja UDP 예제의 로컬 tagasi_saatma_sild server_VALUE')
    sõeluma_VALUE.add_argument('--port', type=int, default=9000)
    parameeter_argument = sõeluma_VALUE.parse_args()
    if not 1 <= parameeter_argument.port <= 65535: sõeluma_VALUE.error('port_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_VALUE:
        server_VALUE.bind(('127.0.0.1', parameeter_argument.port))
        print('UDP 127.0.0.1:{} Ettevalmistamine. Ctrl+C로 Välju_programm.'.format(parameeter_argument.port), flush=True)
        while True:
            andmed, partner_VALUE = server_VALUE.recvfrom(65535)
            server_VALUE.sendto(andmed, partner_VALUE)

if __name__ == '__main__':
    try: Täida_käsk()
    except KeyboardInterrupt: pass
