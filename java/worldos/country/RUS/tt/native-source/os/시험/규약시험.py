#!/usr/bin/env python3
"""хост libc 없이 연결한 Татарча C 프로그램을 фактик_мәгълүмат ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import виртуаль_машина

урнаштыру = Path(__file__).resolve().parents[1]

def үтәргә_команда():
    үлчәм = {}
    сервер_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_VALUE.bind(('127.0.0.1', 0))
    сервер_VALUE.settimeout(0.1)
    접속번호 = сервер_VALUE.getsockname()[1]
    RECEIVED_мәгълүмат = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                мәгълүмат, адрес = сервер_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_мәгълүмат.append(мәгълүмат)
            сервер_VALUE.sendto(мәгълүмат, адрес)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            машина = виртуаль_машина(урнаштыру / ('build/kernel.' + 종류), 종류)
            try:
                for итерация_VALUE in range(2):
                    машина.команда('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    машина.команда('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                эшләтү = len(машина.LOG_юл)
                машина.직렬.sendall(b'run posixinput\n')
                машина.기다림('POSIX INPUT READY', эшләтү)
                машина.직렬.sendall(b'abcdef')
                출력 = машина.기다림('jkoros> ', эшләтү)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                машина.команда('javac Hello.java', ['Exit: 0'])
                машина.команда('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                машина.команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                үлчәм[종류] = машина.LOG_юл.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Birem/공유 урнаштыру/삭제 수명/адрес саклау_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                машина.Yap()
        assert b'posix-udp' in RECEIVED_мәгълүмат and b'truncate' in RECEIVED_мәгълүмат and b'' in RECEIVED_мәгълүмат
    finally:
        끝냄.set(); 일꾼.join(timeout=2); сервер_VALUE.close()
    үлчәм['host_datagrams'] = [мәгълүмат.decode() for мәгълүмат in RECEIVED_мәгълүмат]
    (урнаштыру / 'build/규약시험.json').write_text(json.dumps(үлчәм, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    үтәргә_команда()
