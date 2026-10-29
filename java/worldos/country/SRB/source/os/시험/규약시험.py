#!/usr/bin/env python3
"""хост libc 없이 연결한 한국어 C 프로그램을 стваран_подаци ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import виртуелно_рачунар

Положај = Path(__file__).resolve().parents[1]

def Изврши_команда():
    ИСХОД = {}
    сервер_вриједност = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_вриједност.bind(('127.0.0.1', 0))
    сервер_вриједност.settimeout(0.1)
    број_порта = сервер_вриједност.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                подаци, адреса = сервер_вриједност.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(подаци)
            сервер_вриједност.sendto(подаци, адреса)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            рачунар = виртуелно_рачунар(Положај / ('build/kernel.' + 종류), 종류)
            try:
                for спринт_вриједност in range(2):
                    рачунар.Наредба('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    рачунар.Наредба('run posixudp ' + str(број_порта), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Покрени = len(рачунар.евиденција_ред)
                рачунар.직렬.sendall(b'run posixinput\n')
                рачунар.чекај_стање('POSIX INPUT READY', Покрени)
                рачунар.직렬.sendall(b'abcdef')
                Излаз = рачунар.чекај_стање('jkoros> ', Покрени)
                assert 'POSIX INPUT PASS' in Излаз and 'Exit: 0' in Излаз, Излаз
                рачунар.Наредба('javac Hello.java', ['Exit: 0'])
                рачунар.Наредба('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                рачунар.Наредба('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ИСХОД[종류] = рачунар.евиденција_ред.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Датотека/공유 Положај/삭제 수명/адреса заштитити_вриједност/UDP/표준 입력/기존 Java', flush=True)
            finally:
                рачунар.Затворен()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); сервер_вриједност.close()
    ИСХОД['host_datagrams'] = [подаци.decode() for подаци in 받은자료]
    (Положај / 'build/규약시험.json').write_text(json.dumps(ИСХОД, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Изврши_команда()
