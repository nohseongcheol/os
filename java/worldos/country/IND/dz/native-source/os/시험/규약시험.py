#!/usr/bin/env python3
"""호스트 libc 없이 연결한 한국어 C 프로그램을 실제 ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import 가상기계

གནས_ས = Path(__file__).resolve().parents[1]

def 실행():
    결과 = {}
    서버 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    서버.bind(('127.0.0.1', 0))
    서버.settimeout(0.1)
    접속번호 = 서버.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                자료, 주소 = 서버.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(자료)
            서버.sendto(자료, 주소)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            기계 = 가상기계(གནས_ས / ('build/kernel.' + 종류), 종류)
            try:
                for 반복 in range(2):
                    기계.བརྡ_བཀོད('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    기계.བརྡ_བཀོད('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                གཡོག_བཀོལ = len(기계.기록)
                기계.직렬.sendall(b'run posixinput\n')
                기계.기다림('POSIX INPUT READY', གཡོག_བཀོལ)
                기계.직렬.sendall(b'abcdef')
                출력 = 기계.기다림('jkoros> ', གཡོག_བཀོལ)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                기계.བརྡ_བཀོད('javac Hello.java', ['Exit: 0'])
                기계.བརྡ_བཀོད('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                기계.བརྡ_བཀོད('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = 기계.기록.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ཡིག_སྣོད/공유 གནས_ས/삭제 수명/주소 보호/UDP/표준 입력/기존 Java', flush=True)
            finally:
                기계.ཁ_བསྡམས()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); 서버.close()
    결과['host_datagrams'] = [자료.decode() for 자료 in 받은자료]
    (གནས_ས / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    실행()
