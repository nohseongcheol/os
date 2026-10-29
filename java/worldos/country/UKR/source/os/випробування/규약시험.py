#!/usr/bin/env python3
"""хост libc 없이 연결한 українська C 프로그램을 фактично_дані ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import ВМ

позиція = Path(__file__).resolve().parents[1]

def Виконати_команда():
    результат = {}
    сервер_значення = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_значення.bind(('127.0.0.1', 0))
    сервер_значення.settimeout(0.1)
    номер_порту = сервер_значення.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def відлуння_відповідь():
        while not 끝냄.is_set():
            try:
                дані, Адреса = сервер_значення.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(дані)
            сервер_значення.sendto(дані, Адреса)
    일꾼 = threading.Thread(target=відлуння_відповідь, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            комп_ютер = ВМ(позиція / ('build/kernel.' + 종류), 종류)
            try:
                for спринт_значення in range(2):
                    комп_ютер.команда('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    комп_ютер.команда('run posixudp ' + str(номер_порту), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                запустити = len(комп_ютер.журнал_запис)
                комп_ютер.직렬.sendall(b'run posixinput\n')
                комп_ютер.стан_очікування('POSIX INPUT READY', запустити)
                комп_ютер.직렬.sendall(b'abcdef')
                Вивід = комп_ютер.стан_очікування('jkoros> ', запустити)
                assert 'POSIX INPUT PASS' in Вивід and 'Exit: 0' in Вивід, Вивід
                комп_ютер.команда('javac Hello.java', ['Exit: 0'])
                комп_ютер.команда('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                комп_ютер.команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                результат[종류] = комп_ютер.журнал_запис.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX файл/공유 позиція/삭제 수명/Адреса захищати_значення/UDP/표준 입력/기존 Java', flush=True)
            finally:
                комп_ютер.Закрити()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); сервер_значення.close()
    результат['host_datagrams'] = [дані.decode() for дані in 받은자료]
    (позиція / 'build/규약시험.json').write_text(json.dumps(результат, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Виконати_команда()
