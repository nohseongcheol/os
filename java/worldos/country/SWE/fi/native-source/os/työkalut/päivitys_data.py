#!/usr/bin/env python3
"""isäntä 루프백 주소에만 바인딩하는 UDP testit palvelin_ARVO. Ctrl+C로 종료한다."""
import argparse
import socket

def Suorita_komento():
    jäsentää_ARVO = argparse.ArgumentParser(description='jkoros käyttäjätila UDP 예제의 로컬 palauttaa_silta palvelin_ARVO')
    jäsentää_ARVO.add_argument('--port', type=int, default=9000)
    parametri_argumentti = jäsentää_ARVO.parse_args()
    if not 1 <= parametri_argumentti.port <= 65535: jäsentää_ARVO.error('portti_ARVO 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as palvelin_ARVO:
        palvelin_ARVO.bind(('127.0.0.1', parametri_argumentti.port))
        print('UDP 127.0.0.1:{} Valmistele. Ctrl+C로 Lopeta_ohjelma.'.format(parametri_argumentti.port), flush=True)
        while True:
            data, vertaissolmu_ARVO = palvelin_ARVO.recvfrom(65535)
            palvelin_ARVO.sendto(data, vertaissolmu_ARVO)

if __name__ == '__main__':
    try: Suorita_komento()
    except KeyboardInterrupt: pass
