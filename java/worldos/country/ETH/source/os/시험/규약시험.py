#!/usr/bin/env python3
"""አዘጋጅ_b78e430d libc 없이 연결한 አማርኛ C 프로그램을 ትክክለኛ_ውሂብ ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import ምናባዊ_ማሽን

አካባቢ = Path(__file__).resolve().parents[1]

def ፈጽም_ትእዛዝ():
    ልኬት = {}
    አገልጋይ_እሴት = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    አገልጋይ_እሴት.bind(('127.0.0.1', 0))
    አገልጋይ_እሴት.settimeout(0.1)
    የወደብ_ቁጥር = አገልጋይ_እሴት.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ውሂብ, አድራሻ = አገልጋይ_እሴት.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(ውሂብ)
            አገልጋይ_እሴት.sendto(ውሂብ, አድራሻ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ማሽን = ምናባዊ_ማሽን(አካባቢ / ('build/kernel.' + 종류), 종류)
            try:
                for ሽምጥ_እሴት in range(2):
                    ማሽን.ትእዛዝ('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    ማሽን.ትእዛዝ('run posixudp ' + str(የወደብ_ቁጥር), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ማስኬጃ = len(ማሽን.መዝግብ_ረድፍ)
                ማሽን.직렬.sendall(b'run posixinput\n')
                ማሽን.መጠበቅ_ዞን('POSIX INPUT READY', ማስኬጃ)
                ማሽን.직렬.sendall(b'abcdef')
                ውጤት = ማሽን.መጠበቅ_ዞን('jkoros> ', ማስኬጃ)
                assert 'POSIX INPUT PASS' in ውጤት and 'Exit: 0' in ውጤት, ውጤት
                ማሽን.ትእዛዝ('javac Hello.java', ['Exit: 0'])
                ማሽን.ትእዛዝ('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                ማሽን.ትእዛዝ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ልኬት[종류] = ማሽን.መዝግብ_ረድፍ.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ፋይል/공유 አካባቢ/삭제 수명/አድራሻ ጠብቅ_እሴት/UDP/표준 입력/기존 Java', flush=True)
            finally:
                ማሽን.መዝጊያ()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); አገልጋይ_እሴት.close()
    ልኬት['host_datagrams'] = [ውሂብ.decode() for ውሂብ in 받은자료]
    (አካባቢ / 'build/규약시험.json').write_text(json.dumps(ልኬት, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ፈጽም_ትእዛዝ()
