#!/usr/bin/env python3
"""кабылдоо libc 없이 연결한 한국어 C 프로그램을 актуалдуу_берилмелер ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import виртуалдык_машина

Турган_жери = Path(__file__).resolve().parents[1]

def аткаруу_буйрук():
    결과 = {}
    сервер_маани = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_маани.bind(('127.0.0.1', 0))
    сервер_маани.settimeout(0.1)
    접속번호 = сервер_маани.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                берилмелер, дарек = сервер_маани.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(берилмелер)
            сервер_маани.sendto(берилмелер, дарек)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            машина = виртуалдык_машина(Турган_жери / ('build/kernel.' + 종류), 종류)
            try:
                for итерация_маани in range(2):
                    машина.Команда('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    машина.Команда('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Жүргүзүү = len(машина.жазуу_катар)
                машина.직렬.sendall(b'run posixinput\n')
                машина.기다림('POSIX INPUT READY', Жүргүзүү)
                машина.직렬.sendall(b'abcdef')
                Чыгыш = машина.기다림('jkoros> ', Жүргүзүү)
                assert 'POSIX INPUT PASS' in Чыгыш and 'Exit: 0' in Чыгыш, Чыгыш
                машина.Команда('javac Hello.java', ['Exit: 0'])
                машина.Команда('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                машина.Команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = машина.жазуу_катар.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Файл/공유 Турган_жери/삭제 수명/дарек коргоо_маани/UDP/표준 입력/기존 Java', flush=True)
            finally:
                машина.Жабуу()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); сервер_маани.close()
    결과['host_datagrams'] = [берилмелер.decode() for берилмелер in 받은자료]
    (Турган_жери / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    аткаруу_буйрук()
