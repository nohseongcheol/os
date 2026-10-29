#!/usr/bin/env python3
"""باقار libc 없이 연결한 한국어 C 프로그램을 ھەقىقىي_مەلۇمات ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import مەۋھۇم_ماشىنا

ئورۇن = Path(__file__).resolve().parents[1]

def ئىجرا_قىلىش_بۇيرۇق():
    ئۆلچەم = {}
    مۇلازىمىتېر_قىممىتى = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    مۇلازىمىتېر_قىممىتى.bind(('127.0.0.1', 0))
    مۇلازىمىتېر_قىممىتى.settimeout(0.1)
    접속번호 = مۇلازىمىتېر_قىممىتى.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                مەلۇمات, ئادرېس = مۇلازىمىتېر_قىممىتى.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(مەلۇمات)
            مۇلازىمىتېر_قىممىتى.sendto(مەلۇمات, ئادرېس)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ماشىنا = مەۋھۇم_ماشىنا(ئورۇن / ('build/kernel.' + 종류), 종류)
            try:
                for ئېنتىراتسىيە_قىممىتى in range(2):
                    ماشىنا.بۇيرۇق('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    ماشىنا.بۇيرۇق('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ئىجرا_قىل_2 = len(ماشىنا.خاتىرە_قۇر)
                ماشىنا.직렬.sendall(b'run posixinput\n')
                ماشىنا.기다림('POSIX INPUT READY', ئىجرا_قىل_2)
                ماشىنا.직렬.sendall(b'abcdef')
                چىقار = ماشىنا.기다림('jkoros> ', ئىجرا_قىل_2)
                assert 'POSIX INPUT PASS' in چىقار and 'Exit: 0' in چىقار, چىقار
                ماشىنا.بۇيرۇق('javac Hello.java', ['Exit: 0'])
                ماشىنا.بۇيرۇق('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                ماشىنا.بۇيرۇق('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ئۆلچەم[종류] = ماشىنا.خاتىرە_قۇر.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ھۆججەت/공유 ئورۇن/삭제 수명/ئادرېس قوغدىماق_قىممىتى/UDP/표준 입력/기존 Java', flush=True)
            finally:
                ماشىنا.ياپ()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); مۇلازىمىتېر_قىممىتى.close()
    ئۆلچەم['host_datagrams'] = [مەلۇمات.decode() for مەلۇمات in 받은자료]
    (ئورۇن / 'build/규약시험.json').write_text(json.dumps(ئۆلچەم, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ئىجرا_قىلىش_بۇيرۇق()
