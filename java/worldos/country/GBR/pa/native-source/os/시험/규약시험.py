#!/usr/bin/env python3
"""ਹੋਸਟ libc 없이 연결한 ਪੰਜਾਬੀ C 프로그램을 ਅਸਲ_ਸਮੱਗਰੀ ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import ਵਰਚੁਅਲ_ਮਸ਼ੀਨ

ਸਥਿਤੀ = Path(__file__).resolve().parents[1]

def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼():
    ਮਾਪ = {}
    ਸਰਵਰ_ਕੀਮਤ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ਸਰਵਰ_ਕੀਮਤ.bind(('127.0.0.1', 0))
    ਸਰਵਰ_ਕੀਮਤ.settimeout(0.1)
    접속번호 = ਸਰਵਰ_ਕੀਮਤ.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ਸਮੱਗਰੀ, ਪਤਾ = ਸਰਵਰ_ਕੀਮਤ.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(ਸਮੱਗਰੀ)
            ਸਰਵਰ_ਕੀਮਤ.sendto(ਸਮੱਗਰੀ, ਪਤਾ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ਮਸ਼ੀਨ = ਵਰਚੁਅਲ_ਮਸ਼ੀਨ(ਸਥਿਤੀ / ('build/kernel.' + 종류), 종류)
            try:
                for ਦੋਹਰਾਵ_ਕੀਮਤ in range(2):
                    ਮਸ਼ੀਨ.ਕਮਾਂਡ('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    ਮਸ਼ੀਨ.ਕਮਾਂਡ('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ਚਲਾਓ_2 = len(ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ)
                ਮਸ਼ੀਨ.직렬.sendall(b'run posixinput\n')
                ਮਸ਼ੀਨ.기다림('POSIX INPUT READY', ਚਲਾਓ_2)
                ਮਸ਼ੀਨ.직렬.sendall(b'abcdef')
                ਆਉਟਪੁੱਟ = ਮਸ਼ੀਨ.기다림('jkoros> ', ਚਲਾਓ_2)
                assert 'POSIX INPUT PASS' in ਆਉਟਪੁੱਟ and 'Exit: 0' in ਆਉਟਪੁੱਟ, ਆਉਟਪੁੱਟ
                ਮਸ਼ੀਨ.ਕਮਾਂਡ('javac Hello.java', ['Exit: 0'])
                ਮਸ਼ੀਨ.ਕਮਾਂਡ('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                ਮਸ਼ੀਨ.ਕਮਾਂਡ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ਮਾਪ[종류] = ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ਫਾਇਲ/공유 ਸਥਿਤੀ/삭제 수명/ਪਤਾ ਰੱਖਿਆ_ਕਰਨੀ_ਕੀਮਤ/UDP/표준 입력/기존 Java', flush=True)
            finally:
                ਮਸ਼ੀਨ.ਬੰਦ_ਕਰੋ()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); ਸਰਵਰ_ਕੀਮਤ.close()
    ਮਾਪ['host_datagrams'] = [ਸਮੱਗਰੀ.decode() for ਸਮੱਗਰੀ in 받은자료]
    (ਸਥਿਤੀ / 'build/규약시험.json').write_text(json.dumps(ਮਾਪ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
