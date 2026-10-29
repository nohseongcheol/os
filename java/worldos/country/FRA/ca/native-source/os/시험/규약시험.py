#!/usr/bin/env python3
"""allotjar libc 없이 연결한 Català C 프로그램을 real_dades ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import màquina_virtual

Posició = Path(__file__).resolve().parents[1]

def Executa_ordre():
    RESULTAT = {}
    servidor_VALOR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_VALOR.bind(('127.0.0.1', 0))
    servidor_VALOR.settimeout(0.1)
    número_de_port = servidor_VALOR.getsockname()[1]
    CANTIDAD_RECIBIDA_dades = []
    끝냄 = threading.Event()
    def eco_resposta():
        while not 끝냄.is_set():
            try:
                dades, Adreça = servidor_VALOR.recvfrom(4096)
            except socket.timeout:
                continue
            CANTIDAD_RECIBIDA_dades.append(dades)
            servidor_VALOR.sendto(dades, Adreça)
    일꾼 = threading.Thread(target=eco_resposta, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            màquina = màquina_virtual(Posició / ('build/kernel.' + 종류), 종류)
            try:
                for esprint_VALOR in range(2):
                    màquina.Ordre('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    màquina.Ordre('run posixudp ' + str(número_de_port), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Executa_2 = len(màquina.LOG_fila)
                màquina.직렬.sendall(b'run posixinput\n')
                màquina.Espera_Estat('POSIX INPUT READY', Executa_2)
                màquina.직렬.sendall(b'abcdef')
                Sortida = màquina.Espera_Estat('jkoros> ', Executa_2)
                assert 'POSIX INPUT PASS' in Sortida and 'Exit: 0' in Sortida, Sortida
                màquina.Ordre('javac Hello.java', ['Exit: 0'])
                màquina.Ordre('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                màquina.Ordre('run hello recovered', ['arg: recovered', 'Exit: 0'])
                RESULTAT[종류] = màquina.LOG_fila.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Fitxer/공유 Posició/삭제 수명/Adreça protegir_VALOR/UDP/표준 입력/기존 Java', flush=True)
            finally:
                màquina.Tanca()
        assert b'posix-udp' in CANTIDAD_RECIBIDA_dades and b'truncate' in CANTIDAD_RECIBIDA_dades and b'' in CANTIDAD_RECIBIDA_dades
    finally:
        끝냄.set(); 일꾼.join(timeout=2); servidor_VALOR.close()
    RESULTAT['host_datagrams'] = [dades.decode() for dades in CANTIDAD_RECIBIDA_dades]
    (Posició / 'build/규약시험.json').write_text(json.dumps(RESULTAT, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Executa_ordre()
