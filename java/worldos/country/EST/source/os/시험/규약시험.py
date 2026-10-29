#!/usr/bin/env python3
"""host libc 없이 연결한 Eesti C 프로그램을 tegelik_andmed ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import VM

Asukoht = Path(__file__).resolve().parents[1]

def Täida_käsk():
    TULEMUS = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    pordinumber = server_VALUE.getsockname()[1]
    RECEIVED_andmed = []
    끝냄 = threading.Event()
    def kaja_vastus():
        while not 끝냄.is_set():
            try:
                andmed, ADDRESS = server_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_andmed.append(andmed)
            server_VALUE.sendto(andmed, ADDRESS)
    töötaja_VALUE = threading.Thread(target=kaja_vastus, daemon=True)
    töötaja_VALUE.start()
    try:
        for 종류 in ('elf', 'iso'):
            arvuti = VM(Asukoht / ('build/kernel.' + 종류), 종류)
            try:
                for sprint_VALUE in range(2):
                    arvuti.Käsk('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    arvuti.Käsk('run posixudp ' + str(pordinumber), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Käivita_2 = len(arvuti.LOG_kirje)
                arvuti.직렬.sendall(b'run posixinput\n')
                arvuti.ooteolek('POSIX INPUT READY', Käivita_2)
                arvuti.직렬.sendall(b'abcdef')
                Väljund = arvuti.ooteolek('jkoros> ', Käivita_2)
                assert 'POSIX INPUT PASS' in Väljund and 'Exit: 0' in Väljund, Väljund
                arvuti.Käsk('javac Hello.java', ['Exit: 0'])
                arvuti.Käsk('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                arvuti.Käsk('run hello recovered', ['arg: recovered', 'Exit: 0'])
                TULEMUS[종류] = arvuti.LOG_kirje.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Fail/공유 Asukoht/삭제 수명/ADDRESS kaitsma_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                arvuti.Suletud()
        assert b'posix-udp' in RECEIVED_andmed and b'truncate' in RECEIVED_andmed and b'' in RECEIVED_andmed
    finally:
        끝냄.set(); töötaja_VALUE.join(timeout=2); server_VALUE.close()
    TULEMUS['host_datagrams'] = [andmed.decode() for andmed in RECEIVED_andmed]
    (Asukoht / 'build/규약시험.json').write_text(json.dumps(TULEMUS, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Täida_käsk()
