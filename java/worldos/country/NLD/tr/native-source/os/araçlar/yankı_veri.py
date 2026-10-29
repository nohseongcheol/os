#!/usr/bin/env python3
"""konak 루프백 주소에만 바인딩하는 UDP sınamalar sunucu_değer. Ctrl+C로 종료한다."""
import argparse
import socket

def yürütmek_komut():
    ayrıştırmak_değer = argparse.ArgumentParser(description='jkoros kullanıcı_alanı UDP 예제의 로컬 İade_köprü sunucu_değer')
    ayrıştırmak_değer.add_argument('--port', type=int, default=9000)
    parametre_bağımsız_değişken = ayrıştırmak_değer.parse_args()
    if not 1 <= parametre_bağımsız_değişken.port <= 65535: ayrıştırmak_değer.error('taşımak_değer 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sunucu_değer:
        sunucu_değer.bind(('127.0.0.1', parametre_bağımsız_değişken.port))
        print('UDP 127.0.0.1:{} Hazırlan. Ctrl+C로 Çıkış_program.'.format(parametre_bağımsız_değişken.port), flush=True)
        while True:
            veri, eş_değer = sunucu_değer.recvfrom(65535)
            sunucu_değer.sendto(veri, eş_değer)

if __name__ == '__main__':
    try: yürütmek_komut()
    except KeyboardInterrupt: pass
