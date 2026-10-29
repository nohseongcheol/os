#!/usr/bin/env python3
"""umsingathi 루프백 주소에만 바인딩하는 UDP 시험 iseva_ixabiso. Ctrl+C로 종료한다."""
import argparse
import socket

def ukwenza_umyalelo():
    ingcaciso_yegama_ixabiso = argparse.ArgumentParser(description='jkoros umsebenzisi UDP 예제의 로컬 되돌림 iseva_ixabiso')
    ingcaciso_yegama_ixabiso.add_argument('--port', type=int, default=9000)
    인자 = ingcaciso_yegama_ixabiso.parse_args()
    if not 1 <= 인자.port <= 65535: ingcaciso_yegama_ixabiso.error('iphothi_ixabiso 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as iseva_ixabiso:
        iseva_ixabiso.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} lungisa. Ctrl+C로 phuma_inkqubo.'.format(인자.port), flush=True)
        while True:
            iingcombolo, untanga_ixabiso = iseva_ixabiso.recvfrom(65535)
            iseva_ixabiso.sendto(iingcombolo, untanga_ixabiso)

if __name__ == '__main__':
    try: ukwenza_umyalelo()
    except KeyboardInterrupt: pass
