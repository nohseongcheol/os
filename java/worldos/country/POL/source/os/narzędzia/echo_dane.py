#!/usr/bin/env python3
"""host 루프백 주소에만 바인딩하는 UDP testy serwer_WARTOŚĆ. Ctrl+C로 종료한다."""
import argparse
import socket

def Wykonaj_polecenie():
    analizować_WARTOŚĆ = argparse.ArgumentParser(description='jkoros przestrzeń_użytkownika UDP 예제의 로컬 Zwrot_mostek serwer_WARTOŚĆ')
    analizować_WARTOŚĆ.add_argument('--port', type=int, default=9000)
    parametr_argument = analizować_WARTOŚĆ.parse_args()
    if not 1 <= parametr_argument.port <= 65535: analizować_WARTOŚĆ.error('port_WARTOŚĆ 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as serwer_WARTOŚĆ:
        serwer_WARTOŚĆ.bind(('127.0.0.1', parametr_argument.port))
        print('UDP 127.0.0.1:{} Przygotuj. Ctrl+C로 wyjść_program.'.format(parametr_argument.port), flush=True)
        while True:
            dane, węzeł_równorzędny_WARTOŚĆ = serwer_WARTOŚĆ.recvfrom(65535)
            serwer_WARTOŚĆ.sendto(dane, węzeł_równorzędny_WARTOŚĆ)

if __name__ == '__main__':
    try: Wykonaj_polecenie()
    except KeyboardInterrupt: pass
