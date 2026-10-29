#!/usr/bin/env python3
"""მასპინძელი libc 없이 연결한 한국어 C 프로그램을 რეალური_მონაცემები ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import ვირტუალური_კომპიუტერი

პოზიცია = Path(__file__).resolve().parents[1]

def შესრულება_ბრძანება():
    გაზომვა = {}
    სერვერი_მნიშვნელობა = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    სერვერი_მნიშვნელობა.bind(('127.0.0.1', 0))
    სერვერი_მნიშვნელობა.settimeout(0.1)
    접속번호 = სერვერი_მნიშვნელობა.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                მონაცემები, მისამართი = სერვერი_მნიშვნელობა.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(მონაცემები)
            სერვერი_მნიშვნელობა.sendto(მონაცემები, მისამართი)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            კომპიუტერი = ვირტუალური_კომპიუტერი(პოზიცია / ('build/kernel.' + 종류), 종류)
            try:
                for იტერაცია_მნიშვნელობა in range(2):
                    კომპიუტერი.ბრძანება('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    კომპიუტერი.ბრძანება('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                გაშვება = len(კომპიუტერი.ჟურნალი_ჩაწერა)
                კომპიუტერი.직렬.sendall(b'run posixinput\n')
                კომპიუტერი.მოლოდინი_სტატუსი('POSIX INPUT READY', გაშვება)
                კომპიუტერი.직렬.sendall(b'abcdef')
                출력 = კომპიუტერი.მოლოდინი_სტატუსი('jkoros> ', გაშვება)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                კომპიუტერი.ბრძანება('javac Hello.java', ['Exit: 0'])
                კომპიუტერი.ბრძანება('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                კომპიუტერი.ბრძანება('run hello recovered', ['arg: recovered', 'Exit: 0'])
                გაზომვა[종류] = კომპიუტერი.ჟურნალი_ჩაწერა.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ფაილი/공유 პოზიცია/삭제 수명/მისამართი დაცვა_მნიშვნელობა/UDP/표준 입력/기존 Java', flush=True)
            finally:
                კომპიუტერი.დახურვა()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); სერვერი_მნიშვნელობა.close()
    გაზომვა['host_datagrams'] = [მონაცემები.decode() for მონაცემები in 받은자료]
    (პოზიცია / 'build/규약시험.json').write_text(json.dumps(გაზომვა, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    შესრულება_ბრძანება()
