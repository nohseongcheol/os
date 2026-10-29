#!/usr/bin/env python3
"""host 루프백 주소에만 바인딩하는 UDP 시험 server_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def icra_etmək_əmr():
    parselləmək_VALUE = argparse.ArgumentParser(description='jkoros istifadəçi UDP 예제의 로컬 geri_qaytarmaq_körpü server_VALUE')
    parselləmək_VALUE.add_argument('--port', type=int, default=9000)
    인자 = parselləmək_VALUE.parse_args()
    if not 1 <= 인자.port <= 65535: parselləmək_VALUE.error('port_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_VALUE:
        server_VALUE.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} Hazırla. Ctrl+C로 Çıxış_proqram.'.format(인자.port), flush=True)
        while True:
            verilənlər, eynisəviyyəli_VALUE = server_VALUE.recvfrom(65535)
            server_VALUE.sendto(verilənlər, eynisəviyyəli_VALUE)

if __name__ == '__main__':
    try: icra_etmək_əmr()
    except KeyboardInterrupt: pass
