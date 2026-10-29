#!/usr/bin/env python3
"""хост_рачунар libc 없이 연결한 한국어 C 프로그램을 стваран_подаци ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import 가상기계

위치 = Path(__file__).resolve().parents[1]

def 실행():
    결과 = {}
    сервер_вриједност = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_вриједност.bind(('127.0.0.1', 0))
    сервер_вриједност.settimeout(0.1)
    접속번호 = сервер_вриједност.getsockname()[1]
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
            기계 = 가상기계(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for понављање_вриједност in range(2):
                    기계.команда('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    기계.команда('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                시작 = len(기계.дневник_рада_ред)
                기계.직렬.sendall(b'run posixinput\n')
                기계.기다림('POSIX INPUT READY', 시작)
                기계.직렬.sendall(b'abcdef')
                출력 = 기계.기다림('jkoros> ', 시작)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                기계.команда('javac Hello.java', ['Exit: 0'])
                기계.команда('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                기계.команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = 기계.дневник_рада_ред.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX фајл/공유 위치/삭제 수명/адреса заштитити_вриједност/UDP/표준 입력/기존 Java', flush=True)
            finally:
                기계.затворити()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); сервер_вриједност.close()
    결과['host_datagrams'] = [подаци.decode() for подаци in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    실행()
