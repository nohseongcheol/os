#!/usr/bin/env python3
"""host libc 없이 연결한 Português C 프로그램을 real_dados ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from teste_Usenet import VM

posição = Path(__file__).resolve().parents[1]

def Executar_comando():
    resultado = {}
    servidor_VALOR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_VALOR.bind(('127.0.0.1', 0))
    servidor_VALOR.settimeout(0.1)
    número_da_porta = servidor_VALOR.getsockname()[1]
    RECEBER_dados = []
    끝냄 = threading.Event()
    def eco_resposta():
        while not 끝냄.is_set():
            try:
                dados, Endereço = servidor_VALOR.recvfrom(4096)
            except socket.timeout:
                continue
            RECEBER_dados.append(dados)
            servidor_VALOR.sendto(dados, Endereço)
    trabalho_VALOR = threading.Thread(target=eco_resposta, daemon=True)
    trabalho_VALOR.start()
    try:
        for Tipo_VALOR in ('elf', 'iso'):
            computador = VM(posição / ('build/kernel.' + Tipo_VALOR), Tipo_VALOR)
            try:
                for sprint_VALOR in range(2):
                    computador.comando('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    computador.comando('run posixudp ' + str(número_da_porta), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                iniciar = len(computador.LOG_linha)
                computador.직렬.sendall(b'run posixinput\n')
                computador.estado_de_espera('POSIX INPUT READY', iniciar)
                computador.직렬.sendall(b'abcdef')
                saídaTexto = computador.estado_de_espera('jkoros> ', iniciar)
                assert 'POSIX INPUT PASS' in saídaTexto and 'Exit: 0' in saídaTexto, saídaTexto
                computador.comando('javac Hello.java', ['Exit: 0'])
                computador.comando('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                computador.comando('run hello recovered', ['arg: recovered', 'Exit: 0'])
                resultado[Tipo_VALOR] = computador.LOG_linha.decode('utf-8', 'replace')
                print('PASS:', Tipo_VALOR, 'POSIX ficheiro/공유 posição/삭제 수명/Endereço proteger_VALOR/UDP/표준 entrada_VALOR/기존 Java', flush=True)
            finally:
                computador.Fechar()
        assert b'posix-udp' in RECEBER_dados and b'truncate' in RECEBER_dados and b'' in RECEBER_dados
    finally:
        끝냄.set(); trabalho_VALOR.join(timeout=2); servidor_VALOR.close()
    resultado['host_datagrams'] = [dados.decode() for dados in RECEBER_dados]
    (posição / 'build/contrato_teste.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Executar_comando()
