#!/usr/bin/env python3
"""hospedar 루프백 주소에만 바인딩하는 UDP 시험 servidor_VALOR. Ctrl+C로 종료한다."""
import argparse
import socket

def executar_comando():
    analizar_VALOR = argparse.ArgumentParser(description='jkoros usuario UDP 예제의 로컬 devolver_ponte servidor_VALOR')
    analizar_VALOR.add_argument('--port', type=int, default=9000)
    parámetro_argumento = analizar_VALOR.parse_args()
    if not 1 <= parámetro_argumento.port <= 65535: analizar_VALOR.error('porto_VALOR 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor_VALOR:
        servidor_VALOR.bind(('127.0.0.1', parámetro_argumento.port))
        print('UDP 127.0.0.1:{} 준비. Ctrl+C로 saír_apl.'.format(parámetro_argumento.port), flush=True)
        while True:
            datos, punto_VALOR = servidor_VALOR.recvfrom(65535)
            servidor_VALOR.sendto(datos, punto_VALOR)

if __name__ == '__main__':
    try: executar_comando()
    except KeyboardInterrupt: pass
