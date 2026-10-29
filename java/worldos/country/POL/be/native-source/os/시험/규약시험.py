#!/usr/bin/env python3
"""вузел libc 없이 연결한 한국어 C 프로그램을 фактычны_дадзеныя ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import віртуальны_камп_ютар

Пазіцыя = Path(__file__).resolve().parents[1]

def выканаць_каманда():
    결과 = {}
    сервер_значэнне = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_значэнне.bind(('127.0.0.1', 0))
    сервер_значэнне.settimeout(0.1)
    нумар_порта = сервер_значэнне.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                дадзеныя, адрас = сервер_значэнне.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(дадзеныя)
            сервер_значэнне.sendto(дадзеныя, адрас)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            камп_ютар = віртуальны_камп_ютар(Пазіцыя / ('build/kernel.' + 종류), 종류)
            try:
                for спрынт_значэнне in range(2):
                    камп_ютар.Загад('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    камп_ютар.Загад('run posixudp ' + str(нумар_порта), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Выканаць = len(камп_ютар.журнал_запіс)
                камп_ютар.직렬.sendall(b'run posixinput\n')
                камп_ютар.чакае_стан('POSIX INPUT READY', Выканаць)
                камп_ютар.직렬.sendall(b'abcdef')
                Выхад = камп_ютар.чакае_стан('jkoros> ', Выканаць)
                assert 'POSIX INPUT PASS' in Выхад and 'Exit: 0' in Выхад, Выхад
                камп_ютар.Загад('javac Hello.java', ['Exit: 0'])
                камп_ютар.Загад('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                камп_ютар.Загад('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = камп_ютар.журнал_запіс.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Файл/공유 Пазіцыя/삭제 수명/адрас ахоўваць_значэнне/UDP/표준 입력/기존 Java', flush=True)
            finally:
                камп_ютар.Закрыць()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); сервер_значэнне.close()
    결과['host_datagrams'] = [дадзеныя.decode() for дадзеныя in 받은자료]
    (Пазіцыя / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    выканаць_каманда()
