#!/usr/bin/env python3
"""хост libc 없이 연결한 Български C 프로그램을 действителен_данни ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import виртуална_машина

Позиция = Path(__file__).resolve().parents[1]

def изпълнявам_команда():
    РЕЗУЛТАТ = {}
    сървър_стойност = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сървър_стойност.bind(('127.0.0.1', 0))
    сървър_стойност.settimeout(0.1)
    номер_на_порт = сървър_стойност.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def Ехо_отговор():
        while not 끝냄.is_set():
            try:
                данни, адрес = сървър_стойност.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(данни)
            сървър_стойност.sendto(данни, адрес)
    일꾼 = threading.Thread(target=Ехо_отговор, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            машина = виртуална_машина(Позиция / ('build/kernel.' + 종류), 종류)
            try:
                for спринт_стойност in range(2):
                    машина.Команда('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    машина.Команда('run posixudp ' + str(номер_на_порт), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Стартиране = len(машина.регистрирам_запис)
                машина.직렬.sendall(b'run posixinput\n')
                машина.състояние_на_изчакване('POSIX INPUT READY', Стартиране)
                машина.직렬.sendall(b'abcdef')
                Изход = машина.състояние_на_изчакване('jkoros> ', Стартиране)
                assert 'POSIX INPUT PASS' in Изход and 'Exit: 0' in Изход, Изход
                машина.Команда('javac Hello.java', ['Exit: 0'])
                машина.Команда('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                машина.Команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                РЕЗУЛТАТ[종류] = машина.регистрирам_запис.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Файл/공유 Позиция/삭제 수명/адрес защитавам_стойност/UDP/표준 입력/기존 Java', flush=True)
            finally:
                машина.Затворен()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); сървър_стойност.close()
    РЕЗУЛТАТ['host_datagrams'] = [данни.decode() for данни in 받은자료]
    (Позиция / 'build/규약시험.json').write_text(json.dumps(РЕЗУЛТАТ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    изпълнявам_команда()
