#!/usr/bin/env python3
"""አዐንግድ libc 없이 연결한 ትግርኛ C 프로그램을 ትኽክለኛ_ሓበሬታ ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import መሳሊ_ማሽን

위치 = Path(__file__).resolve().parents[1]

def ተግብር_ትእዛዝ():
    결과 = {}
    ኣገልጋሊ_ዋጋ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ኣገልጋሊ_ዋጋ.bind(('127.0.0.1', 0))
    ኣገልጋሊ_ዋጋ.settimeout(0.1)
    접속번호 = ኣገልጋሊ_ዋጋ.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ሓበሬታ, ኣድራሻ = ኣገልጋሊ_ዋጋ.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(ሓበሬታ)
            ኣገልጋሊ_ዋጋ.sendto(ሓበሬታ, ኣድራሻ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ማሽን = መሳሊ_ማሽን(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for ዝርዝር_ዋጋ in range(2):
                    ማሽን.ትእዛዝ('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    ማሽን.ትእዛዝ('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ኣኺድ = len(ማሽን.ምዝጉብ_ሪጋ)
                ማሽን.직렬.sendall(b'run posixinput\n')
                ማሽን.기다림('POSIX INPUT READY', ኣኺድ)
                ማሽን.직렬.sendall(b'abcdef')
                출력 = ማሽን.기다림('jkoros> ', ኣኺድ)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                ማሽን.ትእዛዝ('javac Hello.java', ['Exit: 0'])
                ማሽን.ትእዛዝ('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                ማሽን.ትእዛዝ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = ማሽን.ምዝጉብ_ሪጋ.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ፋይል/공유 위치/삭제 수명/ኣድራሻ ሓልው_ዋጋ/UDP/표준 입력/기존 Java', flush=True)
            finally:
                ማሽን.ዕጸው()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); ኣገልጋሊ_ዋጋ.close()
    결과['host_datagrams'] = [ሓበሬታ.decode() for ሓበሬታ in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ተግብር_ትእዛዝ()
