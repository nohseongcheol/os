#!/usr/bin/env python3
"""vært 루프백 주소에만 바인딩하는 UDP 시험 server_VÆRDI. Ctrl+C로 종료한다."""
import argparse
import socket

def Udfør_kommando():
    opdele_tekst_VÆRDI = argparse.ArgumentParser(description='jkoros bruger UDP 예제의 로컬 returnere_bro server_VÆRDI')
    opdele_tekst_VÆRDI.add_argument('--port', type=int, default=9000)
    parameter_argument = opdele_tekst_VÆRDI.parse_args()
    if not 1 <= parameter_argument.port <= 65535: opdele_tekst_VÆRDI.error('port_VÆRDI 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_VÆRDI:
        server_VÆRDI.bind(('127.0.0.1', parameter_argument.port))
        print('UDP 127.0.0.1:{} Tilrettelæg. Ctrl+C로 Afslut_app.'.format(parameter_argument.port), flush=True)
        while True:
            data, peer_VÆRDI = server_VÆRDI.recvfrom(65535)
            server_VÆRDI.sendto(data, peer_VÆRDI)

if __name__ == '__main__':
    try: Udfør_kommando()
    except KeyboardInterrupt: pass
