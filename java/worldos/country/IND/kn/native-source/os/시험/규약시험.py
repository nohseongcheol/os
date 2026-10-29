#!/usr/bin/env python3
"""ಹೋಸ್ಟ್ libc 없이 연결한 ಕನ್ನಡ C 프로그램을 ನಿಜವಾದ_ಡೇಟಾ ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import ಅಗೋಚರ_ಯಂತ್ರ

ಸ್ಥಾನ = Path(__file__).resolve().parents[1]

def ಪೂರೈಸು_ಆದೇಶ():
    ಮಾಪನ = {}
    ಸರ್ವರ್_ಮೌಲ್ಯ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ಸರ್ವರ್_ಮೌಲ್ಯ.bind(('127.0.0.1', 0))
    ಸರ್ವರ್_ಮೌಲ್ಯ.settimeout(0.1)
    ಪೋರ್ಟ್_ಸಂಖ್ಯೆ = ಸರ್ವರ್_ಮೌಲ್ಯ.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ಡೇಟಾ, ಇಮೇಲ್ = ಸರ್ವರ್_ಮೌಲ್ಯ.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(ಡೇಟಾ)
            ಸರ್ವರ್_ಮೌಲ್ಯ.sendto(ಡೇಟಾ, ಇಮೇಲ್)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ಯಂತ್ರ = ಅಗೋಚರ_ಯಂತ್ರ(ಸ್ಥಾನ / ('build/kernel.' + 종류), 종류)
            try:
                for ಸ್ಪ್ರಿಂಟ್_ಮೌಲ್ಯ in range(2):
                    ಯಂತ್ರ.ಆಜ್ಞೆ('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    ಯಂತ್ರ.ಆಜ್ಞೆ('run posixudp ' + str(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ಚಲಾಯಿಸು_2 = len(ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ)
                ಯಂತ್ರ.직렬.sendall(b'run posixinput\n')
                ಯಂತ್ರ.ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ('POSIX INPUT READY', ಚಲಾಯಿಸು_2)
                ಯಂತ್ರ.직렬.sendall(b'abcdef')
                ಔಟ್_ಪುಟ್ = ಯಂತ್ರ.ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ('jkoros> ', ಚಲಾಯಿಸು_2)
                assert 'POSIX INPUT PASS' in ಔಟ್_ಪುಟ್ and 'Exit: 0' in ಔಟ್_ಪುಟ್, ಔಟ್_ಪುಟ್
                ಯಂತ್ರ.ಆಜ್ಞೆ('javac Hello.java', ['Exit: 0'])
                ಯಂತ್ರ.ಆಜ್ಞೆ('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                ಯಂತ್ರ.ಆಜ್ಞೆ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ಮಾಪನ[종류] = ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ಕಡತ/공유 ಸ್ಥಾನ/삭제 수명/ಇಮೇಲ್ ರಕ್ಷಿಸಿ_ಮೌಲ್ಯ/UDP/표준 입력/기존 Java', flush=True)
            finally:
                ಯಂತ್ರ.ಮುಚ್ಚು()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); ಸರ್ವರ್_ಮೌಲ್ಯ.close()
    ಮಾಪನ['host_datagrams'] = [ಡೇಟಾ.decode() for ಡೇಟಾ in 받은자료]
    (ಸ್ಥಾನ / 'build/규약시험.json').write_text(json.dumps(ಮಾಪನ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ಪೂರೈಸು_ಆದೇಶ()
