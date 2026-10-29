#!/usr/bin/env python3
"""Wirtssystem 루프백 주소에만 바인딩하는 UDP Prüfungen dienstanbieterWert. Ctrl+C로 종료한다."""
import argparse
import socket

def befehlAusführen():
    wertAnalysieren = argparse.ArgumentParser(description='jkoros Benutzer UDP 예제의 로컬 zurückkehrenBrücke dienstanbieterWert')
    wertAnalysieren.add_argument('--port', type=int, default=9000)
    parameterArgument = wertAnalysieren.parse_args()
    if not 1 <= parameterArgument.port <= 65535: wertAnalysieren.error('portWert 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as dienstanbieterWert:
        dienstanbieterWert.bind(('127.0.0.1', parameterArgument.port))
        print('UDP 127.0.0.1:{} vorbereiten. Ctrl+C로 verlassenProzessProgramm.'.format(parameterArgument.port), flush=True)
        while True:
            Daten, gegenstelleWert = dienstanbieterWert.recvfrom(65535)
            dienstanbieterWert.sendto(Daten, gegenstelleWert)

if __name__ == '__main__':
    try: befehlAusführen()
    except KeyboardInterrupt: pass
