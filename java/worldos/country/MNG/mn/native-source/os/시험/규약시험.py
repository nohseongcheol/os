#!/usr/bin/env python3
"""хост libc 없이 연결한 Монгол C 프로그램을 бодит_өгөгдөл ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import виртуал_компьютер

위치 = Path(__file__).resolve().parents[1]

def Гүйцэтгэх_команд():
    결과 = {}
    сервер_утга = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_утга.bind(('127.0.0.1', 0))
    сервер_утга.settimeout(0.1)
    접속번호 = сервер_утга.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                өгөгдөл, хаяг = сервер_утга.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(өгөгдөл)
            сервер_утга.sendto(өгөгдөл, хаяг)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            компьютер = виртуал_компьютер(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for давталт_утга in range(2):
                    компьютер.Тушаал('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    компьютер.Тушаал('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Ажиллуулах = len(компьютер.бичих_мөр_6e8b375a)
                компьютер.직렬.sendall(b'run posixinput\n')
                компьютер.기다림('POSIX INPUT READY', Ажиллуулах)
                компьютер.직렬.sendall(b'abcdef')
                출력 = компьютер.기다림('jkoros> ', Ажиллуулах)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                компьютер.Тушаал('javac Hello.java', ['Exit: 0'])
                компьютер.Тушаал('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                компьютер.Тушаал('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = компьютер.бичих_мөр_6e8b375a.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Файл/공유 위치/삭제 수명/хаяг хамгаалах_утга/UDP/표준 입력/기존 Java', flush=True)
            finally:
                компьютер.Хаах()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); сервер_утга.close()
    결과['host_datagrams'] = [өгөгдөл.decode() for өгөгдөл in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Гүйцэтгэх_команд()
