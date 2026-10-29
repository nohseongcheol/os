#!/usr/bin/env python3
"""Anfitrión 루프백 주소에만 바인딩하는 UDP Pruebas valorServidor. Ctrl+C로 종료한다."""
import argparse
import socket

def ejecutarComando():
    analizarValor = argparse.ArgumentParser(description='jkoros Usuario UDP 예제의 로컬 puenteRetornar valorServidor')
    analizarValor.add_argument('--port', type=int, default=9000)
    argumentoParámetro = analizarValor.parse_args()
    if not 1 <= argumentoParámetro.port <= 65535: analizarValor.error('valorPuerto 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as valorServidor:
        valorServidor.bind(('127.0.0.1', argumentoParámetro.port))
        print('UDP 127.0.0.1:{} preparar. Ctrl+C로 programaSalir.'.format(argumentoParámetro.port), flush=True)
        while True:
            Datos, valorParRed = valorServidor.recvfrom(65535)
            valorServidor.sendto(Datos, valorParRed)

if __name__ == '__main__':
    try: ejecutarComando()
    except KeyboardInterrupt: pass
