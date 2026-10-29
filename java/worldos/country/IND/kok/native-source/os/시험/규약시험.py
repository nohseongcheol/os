#!/usr/bin/env python3
"""येजमान libc 없이 연결한 한국어 C 프로그램을 प्रत्यक्ष_डेटा ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import भ्रामक_यंत्र

स्थिती = Path(__file__).resolve().parents[1]

def पाळो_दिवचो_आदेश():
    मेजप = {}
    सर्वर_मोल = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    सर्वर_मोल.bind(('127.0.0.1', 0))
    सर्वर_मोल.settimeout(0.1)
    접속번호 = सर्वर_मोल.getsockname()[1]
    RECEIVED_डेटा = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                डेटा, नामो = सर्वर_मोल.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_डेटा.append(डेटा)
            सर्वर_मोल.sendto(डेटा, नामो)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            यंत्र = भ्रामक_यंत्र(स्थिती / ('build/kernel.' + 종류), 종류)
            try:
                for परतवण_मोल in range(2):
                    यंत्र.आदेश('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    यंत्र.आदेश('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                चलोवप = len(यंत्र.LOG_नोंद)
                यंत्र.직렬.sendall(b'run posixinput\n')
                यंत्र.기다림('POSIX INPUT READY', चलोवप)
                यंत्र.직렬.sendall(b'abcdef')
                출력 = यंत्र.기다림('jkoros> ', चलोवप)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                यंत्र.आदेश('javac Hello.java', ['Exit: 0'])
                यंत्र.आदेश('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                यंत्र.आदेश('run hello recovered', ['arg: recovered', 'Exit: 0'])
                मेजप[종류] = यंत्र.LOG_नोंद.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX फायल/공유 स्थिती/삭제 수명/नामो राखचें_मोल/UDP/표준 입력/기존 Java', flush=True)
            finally:
                यंत्र.शेवट()
        assert b'posix-udp' in RECEIVED_डेटा and b'truncate' in RECEIVED_डेटा and b'' in RECEIVED_डेटा
    finally:
        끝냄.set(); 일꾼.join(timeout=2); सर्वर_मोल.close()
    मेजप['host_datagrams'] = [डेटा.decode() for डेटा in RECEIVED_डेटा]
    (स्थिती / 'build/규약시험.json').write_text(json.dumps(मेजप, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    पाळो_दिवचो_आदेश()
