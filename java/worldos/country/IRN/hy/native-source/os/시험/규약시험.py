#!/usr/bin/env python3
"""հոստ libc 없이 연결한 한국어 C 프로그램을 իրական_տվյալ ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import վիրտուալ_մեքենա

Դիրք = Path(__file__).resolve().parents[1]

def կատարել_հրաման():
    չափ = {}
    սպասարկիչ_արժեք = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    սպասարկիչ_արժեք.bind(('127.0.0.1', 0))
    սպասարկիչ_արժեք.settimeout(0.1)
    접속번호 = սպասարկիչ_արժեք.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                տվյալ, հասցե = սպասարկիչ_արժեք.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(տվյալ)
            սպասարկիչ_արժեք.sendto(տվյալ, հասցե)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            մեքենա = վիրտուալ_մեքենա(Դիրք / ('build/kernel.' + 종류), 종류)
            try:
                for բազմակրկնություն_արժեք in range(2):
                    մեքենա.Հրահանգ('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    մեքենա.Հրահանգ('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Գործարկել = len(մեքենա.մատյան_տող)
                մեքենա.직렬.sendall(b'run posixinput\n')
                մեքենա.기다림('POSIX INPUT READY', Գործարկել)
                մեքենա.직렬.sendall(b'abcdef')
                Ելք = մեքենա.기다림('jkoros> ', Գործարկել)
                assert 'POSIX INPUT PASS' in Ելք and 'Exit: 0' in Ելք, Ելք
                մեքենա.Հրահանգ('javac Hello.java', ['Exit: 0'])
                մեքենա.Հրահանգ('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                մեքենա.Հրահանգ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                չափ[종류] = մեքենա.մատյան_տող.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Ֆայլ/공유 Դիրք/삭제 수명/հասցե պաշտպանել_արժեք/UDP/표준 입력/기존 Java', flush=True)
            finally:
                մեքենա.Փակ()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); սպասարկիչ_արժեք.close()
    չափ['host_datagrams'] = [տվյալ.decode() for տվյալ in 받은자료]
    (Դիրք / 'build/규약시험.json').write_text(json.dumps(չափ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    կատարել_հրաման()
