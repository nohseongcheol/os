#!/usr/bin/env python3
"""hospedar libc 없이 연결한 Galego C 프로그램을 real_datos ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import máquina_virtual

Posición = Path(__file__).resolve().parents[1]

def executar_comando():
    RESULTANTE = {}
    servidor_VALOR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_VALOR.bind(('127.0.0.1', 0))
    servidor_VALOR.settimeout(0.1)
    número_do_porto = servidor_VALOR.getsockname()[1]
    RECIBIDO_datos = []
    끝냄 = threading.Event()
    def eco_resposta():
        while not 끝냄.is_set():
            try:
                datos, ENDEREZO = servidor_VALOR.recvfrom(4096)
            except socket.timeout:
                continue
            RECIBIDO_datos.append(datos)
            servidor_VALOR.sendto(datos, ENDEREZO)
    일꾼 = threading.Thread(target=eco_resposta, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            máquina = máquina_virtual(Posición / ('build/kernel.' + 종류), 종류)
            try:
                for sprint_VALOR in range(2):
                    máquina.Orde('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    máquina.Orde('run posixudp ' + str(número_do_porto), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Executar_2 = len(máquina.LOG_fila)
                máquina.직렬.sendall(b'run posixinput\n')
                máquina.agarda_Estado('POSIX INPUT READY', Executar_2)
                máquina.직렬.sendall(b'abcdef')
                Saída = máquina.agarda_Estado('jkoros> ', Executar_2)
                assert 'POSIX INPUT PASS' in Saída and 'Exit: 0' in Saída, Saída
                máquina.Orde('javac Hello.java', ['Exit: 0'])
                máquina.Orde('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                máquina.Orde('run hello recovered', ['arg: recovered', 'Exit: 0'])
                RESULTANTE[종류] = máquina.LOG_fila.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Ficheiro/공유 Posición/삭제 수명/ENDEREZO protexer_VALOR/UDP/표준 입력/기존 Java', flush=True)
            finally:
                máquina.Pechar()
        assert b'posix-udp' in RECIBIDO_datos and b'truncate' in RECIBIDO_datos and b'' in RECIBIDO_datos
    finally:
        끝냄.set(); 일꾼.join(timeout=2); servidor_VALOR.close()
    RESULTANTE['host_datagrams'] = [datos.decode() for datos in RECIBIDO_datos]
    (Posición / 'build/규약시험.json').write_text(json.dumps(RESULTANTE, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    executar_comando()
