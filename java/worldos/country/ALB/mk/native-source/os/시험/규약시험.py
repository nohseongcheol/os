#!/usr/bin/env python3
"""вдоми libc 없이 연결한 Македонски C 프로그램을 реален_податоци ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import виртуелен_машина

Позиција = Path(__file__).resolve().parents[1]

def Изврши_наредба():
    мерка = {}
    сервер_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_VALUE.bind(('127.0.0.1', 0))
    сервер_VALUE.settimeout(0.1)
    број_на_порта = сервер_VALUE.getsockname()[1]
    RECEIVED_податоци = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                податоци, адреса = сервер_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_податоци.append(податоци)
            сервер_VALUE.sendto(податоци, адреса)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            машина = виртуелен_машина(Позиција / ('build/kernel.' + 종류), 종류)
            try:
                for повторување_VALUE in range(2):
                    машина.Команда('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    машина.Команда('run posixudp ' + str(број_на_порта), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Изврши_2 = len(машина.LOG_ред)
                машина.직렬.sendall(b'run posixinput\n')
                машина.почекај_статус('POSIX INPUT READY', Изврши_2)
                машина.직렬.sendall(b'abcdef')
                출력 = машина.почекај_статус('jkoros> ', Изврши_2)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                машина.Команда('javac Hello.java', ['Exit: 0'])
                машина.Команда('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                машина.Команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                мерка[종류] = машина.LOG_ред.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Датотека/공유 Позиција/삭제 수명/адреса заштита_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                машина.Затвори()
        assert b'posix-udp' in RECEIVED_податоци and b'truncate' in RECEIVED_податоци and b'' in RECEIVED_податоци
    finally:
        끝냄.set(); 일꾼.join(timeout=2); сервер_VALUE.close()
    мерка['host_datagrams'] = [податоци.decode() for податоци in RECEIVED_податоци]
    (Позиција / 'build/규약시험.json').write_text(json.dumps(мерка, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Изврши_наредба()
