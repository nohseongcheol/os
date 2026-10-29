#!/usr/bin/env python3
"""орналастыру libc 없이 연결한 한국어 C 프로그램을 нақты_деректер ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import виртуалды_машина

Орны = Path(__file__).resolve().parents[1]

def орындау_пәрмен():
    НӘТИЖЕ = {}
    сервер_мән = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_мән.bind(('127.0.0.1', 0))
    сервер_мән.settimeout(0.1)
    порт_нөмірі = сервер_мән.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def экранға_шығару_жауап():
        while not 끝냄.is_set():
            try:
                деректер, мекенжай = сервер_мән.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(деректер)
            сервер_мән.sendto(деректер, мекенжай)
    일꾼 = threading.Thread(target=экранға_шығару_жауап, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            компьютер = виртуалды_машина(Орны / ('build/kernel.' + 종류), 종류)
            try:
                for спринт_мән in range(2):
                    компьютер.Команда('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    компьютер.Команда('run posixudp ' + str(порт_нөмірі), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Орындау_2 = len(компьютер.журнал_жол)
                компьютер.직렬.sendall(b'run posixinput\n')
                компьютер.күту_күйі('POSIX INPUT READY', Орындау_2)
                компьютер.직렬.sendall(b'abcdef')
                Шығысы = компьютер.күту_күйі('jkoros> ', Орындау_2)
                assert 'POSIX INPUT PASS' in Шығысы and 'Exit: 0' in Шығысы, Шығысы
                компьютер.Команда('javac Hello.java', ['Exit: 0'])
                компьютер.Команда('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                компьютер.Команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                НӘТИЖЕ[종류] = компьютер.журнал_жол.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Файл/공유 Орны/삭제 수명/мекенжай қорғау_мән/UDP/표준 입력/기존 Java', flush=True)
            finally:
                компьютер.Жабу()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); сервер_мән.close()
    НӘТИЖЕ['host_datagrams'] = [деректер.decode() for деректер in 받은자료]
    (Орны / 'build/규약시험.json').write_text(json.dumps(НӘТИЖЕ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    орындау_пәрмен()
