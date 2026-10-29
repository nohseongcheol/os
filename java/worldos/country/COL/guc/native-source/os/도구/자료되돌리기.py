#!/usr/bin/env python3
"""epiajatü 루프백 주소에만 바인딩하는 UDP 시험 서버. Ctrl+C로 종료한다."""
import argparse
import socket

def 실행():
    akatajaa_ajutuu = argparse.ArgumentParser(description='jkoros ka_yataayakalü UDP 예제의 로컬 되돌림 서버')
    akatajaa_ajutuu.add_argument('--port', type=int, default=9000)
    인자 = akatajaa_ajutuu.parse_args()
    if not 1 <= 인자.port <= 65535: akatajaa_ajutuu.error('outtülee_ajutuu 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 서버:
        서버.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} 준비. Ctrl+C로 aju_itaa_akumajiaa.'.format(인자.port), flush=True)
        while True:
            atijaaya, wanaawasü_ajutuu = 서버.recvfrom(65535)
            서버.sendto(atijaaya, wanaawasü_ajutuu)

if __name__ == '__main__':
    try: 실행()
    except KeyboardInterrupt: pass
