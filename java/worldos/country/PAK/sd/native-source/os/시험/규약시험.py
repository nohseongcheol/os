#!/usr/bin/env python3
"""مهمان libc 없이 연결한 한국어 C 프로그램을 اصلي_ڪوائف ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import مجازي_مشين

위치 = Path(__file__).resolve().parents[1]

def تعميل_ڪرڻ_حڪم():
    결과 = {}
    سرور_قدر = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    سرور_قدر.bind(('127.0.0.1', 0))
    سرور_قدر.settimeout(0.1)
    접속번호 = سرور_قدر.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ڪوائف, پتو = سرور_قدر.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(ڪوائف)
            سرور_قدر.sendto(ڪوائف, پتو)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            مشين = مجازي_مشين(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for دهرائڻ_قدر in range(2):
                    مشين.حڪم('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    مشين.حڪم('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                هلائڻ = len(مشين.لاگ_صف)
                مشين.직렬.sendall(b'run posixinput\n')
                مشين.기다림('POSIX INPUT READY', هلائڻ)
                مشين.직렬.sendall(b'abcdef')
                출력 = مشين.기다림('jkoros> ', هلائڻ)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                مشين.حڪم('javac Hello.java', ['Exit: 0'])
                مشين.حڪم('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                مشين.حڪم('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = مشين.لاگ_صف.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX فائل/공유 위치/삭제 수명/پتو حفاظت_ڪريو_قدر/UDP/표준 입력/기존 Java', flush=True)
            finally:
                مشين.بند_ڪرڻ()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); سرور_قدر.close()
    결과['host_datagrams'] = [ڪوائف.decode() for ڪوائف in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    تعميل_ڪرڻ_حڪم()
