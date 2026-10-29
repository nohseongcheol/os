#!/usr/bin/env python3
"""Ostalari 루프백 주소에만 바인딩하는 UDP 시험 zerbitzari_balio. Ctrl+C로 종료한다."""
import argparse
import socket

def exekutatu_komando():
    analizatu_balio = argparse.ArgumentParser(description='jkoros erabiltzaile UDP 예제의 로컬 itzuli_zubi zerbitzari_balio')
    analizatu_balio.add_argument('--port', type=int, default=9000)
    parametro_arg = analizatu_balio.parse_args()
    if not 1 <= parametro_arg.port <= 65535: analizatu_balio.error('ataka_balio 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as zerbitzari_balio:
        zerbitzari_balio.bind(('127.0.0.1', parametro_arg.port))
        print('UDP 127.0.0.1:{} 준비. Ctrl+C로 irten_aplik.'.format(parametro_arg.port), flush=True)
        while True:
            datuak, pareko_balio = zerbitzari_balio.recvfrom(65535)
            zerbitzari_balio.sendto(datuak, pareko_balio)

if __name__ == '__main__':
    try: exekutatu_komando()
    except KeyboardInterrupt: pass
