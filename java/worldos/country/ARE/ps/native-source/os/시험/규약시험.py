#!/usr/bin/env python3
"""کوربه libc 없이 연결한 한국어 C 프로그램을 실제 ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import 가상기계

ځای = Path(__file__).resolve().parents[1]

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
                اومتوک, پته = 서버.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(اومتوک)
            서버.sendto(اومتوک, پته)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            기계 = 가상기계(ځای / ('build/kernel.' + 종류), 종류)
            try:
                for تکرار_ارزښت in range(2):
                    기계.بولۍ('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    기계.بولۍ('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ځغلول = len(기계.خبرال_کیل)
                기계.직렬.sendall(b'run posixinput\n')
                기계.기다림('POSIX INPUT READY', ځغلول)
                기계.직렬.sendall(b'abcdef')
                출력 = 기계.기다림('jkoros> ', ځغلول)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                기계.بولۍ('javac Hello.java', ['Exit: 0'])
                기계.بولۍ('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                기계.بولۍ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = 기계.خبرال_کیل.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX دوتنه/공유 ځای/삭제 수명/پته خونديېل_ارزښت/UDP/표준 입력/기존 Java', flush=True)
            finally:
                기계.بندول()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); 서버.close()
    결과['host_datagrams'] = [اومتوک.decode() for اومتوک in 받은자료]
    (ځای / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    실행()
