#!/usr/bin/env python3
"""узел libc 없이 연결한 русский C 프로그램을 фактический_данные ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from тест_пользователь_сеть import VM

позиция = Path(__file__).resolve().parents[1]

def 실행():
    результат = {}
    сервер_ЗНАЧЕН = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_ЗНАЧЕН.bind(('127.0.0.1', 0))
    сервер_ЗНАЧЕН.settimeout(0.1)
    номер_порта = сервер_ЗНАЧЕН.getsockname()[1]
    ПОЛУЧЕНО_данные = []
    끝냄 = threading.Event()
    def вывод_на_экран_ответ():
        while not 끝냄.is_set():
            try:
                данные, АДРЕС = сервер_ЗНАЧЕН.recvfrom(4096)
            except socket.timeout:
                continue
            ПОЛУЧЕНО_данные.append(данные)
            сервер_ЗНАЧЕН.sendto(данные, АДРЕС)
    работник_ЗНАЧЕН = threading.Thread(target=вывод_на_экран_ответ, daemon=True)
    работник_ЗНАЧЕН.start()
    try:
        for Вид_ЗНАЧЕН in ('elf', 'iso'):
            компьютер_5eb260fa = VM(позиция / ('build/kernel.' + Вид_ЗНАЧЕН), Вид_ЗНАЧЕН)
            try:
                for спринт_ЗНАЧЕН in range(2):
                    компьютер_5eb260fa.команда('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    компьютер_5eb260fa.команда('run posixudp ' + str(номер_порта), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                запустить = len(компьютер_5eb260fa.LOG_ЗАПИСЬ)
                компьютер_5eb260fa.직렬.sendall(b'run posixinput\n')
                компьютер_5eb260fa.состояние_ожидания('POSIX INPUT READY', запустить)
                компьютер_5eb260fa.직렬.sendall(b'abcdef')
                текстовыйВывод = компьютер_5eb260fa.состояние_ожидания('jkoros> ', запустить)
                assert 'POSIX INPUT PASS' in текстовыйВывод and 'Exit: 0' in текстовыйВывод, текстовыйВывод
                компьютер_5eb260fa.команда('javac Hello.java', ['Exit: 0'])
                компьютер_5eb260fa.команда('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                компьютер_5eb260fa.команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                результат[Вид_ЗНАЧЕН] = компьютер_5eb260fa.LOG_ЗАПИСЬ.decode('utf-8', 'replace')
                print('PASS:', Вид_ЗНАЧЕН, 'POSIX файл/공유 позиция/삭제 수명/АДРЕС защитить_ЗНАЧЕН/UDP/표준 входные_данные_ЗНАЧЕН/기존 Java', flush=True)
            finally:
                компьютер_5eb260fa.Закрыть()
        assert b'posix-udp' in ПОЛУЧЕНО_данные and b'truncate' in ПОЛУЧЕНО_данные and b'' in ПОЛУЧЕНО_данные
    finally:
        끝냄.set(); работник_ЗНАЧЕН.join(timeout=2); сервер_ЗНАЧЕН.close()
    результат['host_datagrams'] = [данные.decode() for данные in ПОЛУЧЕНО_данные]
    (позиция / 'build/задание_тест.json').write_text(json.dumps(результат, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    실행()
