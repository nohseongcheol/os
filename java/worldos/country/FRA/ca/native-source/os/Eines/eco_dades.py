#!/usr/bin/env python3
"""allotjar 루프백 주소에만 바인딩하는 UDP 시험 servidor_VALOR. Ctrl+C로 종료한다."""
import argparse
import socket

def Executa_ordre():
    analitzar_VALOR = argparse.ArgumentParser(description='jkoros usuari UDP 예제의 로컬 tornar_les_tasques_pont servidor_VALOR')
    analitzar_VALOR.add_argument('--port', type=int, default=9000)
    paràmetre_arg = analitzar_VALOR.parse_args()
    if not 1 <= paràmetre_arg.port <= 65535: analitzar_VALOR.error('port_VALOR 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor_VALOR:
        servidor_VALOR.bind(('127.0.0.1', paràmetre_arg.port))
        print('UDP 127.0.0.1:{} Prepara. Ctrl+C로 Surt_programa.'.format(paràmetre_arg.port), flush=True)
        while True:
            dades, homòleg_VALOR = servidor_VALOR.recvfrom(65535)
            servidor_VALOR.sendto(dades, homòleg_VALOR)

if __name__ == '__main__':
    try: Executa_ordre()
    except KeyboardInterrupt: pass
