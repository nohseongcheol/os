#!/usr/bin/env python3
"""host 루프백 주소에만 바인딩하는 UDP testes servidor_VALOR. Ctrl+C로 종료한다."""
import argparse
import socket

def Executar_comando():
    analisar_VALOR = argparse.ArgumentParser(description='jkoros espaço_do_utilizador UDP 예제의 로컬 devolver_ponte servidor_VALOR')
    analisar_VALOR.add_argument('--port', type=int, default=9000)
    parâmetro_argumento = analisar_VALOR.parse_args()
    if not 1 <= parâmetro_argumento.port <= 65535: analisar_VALOR.error('porta_VALOR 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor_VALOR:
        servidor_VALOR.bind(('127.0.0.1', parâmetro_argumento.port))
        print('UDP 127.0.0.1:{} Preparar. Ctrl+C로 sair_app.'.format(parâmetro_argumento.port), flush=True)
        while True:
            dados, par_VALOR = servidor_VALOR.recvfrom(65535)
            servidor_VALOR.sendto(dados, par_VALOR)

if __name__ == '__main__':
    try: Executar_comando()
    except KeyboardInterrupt: pass
