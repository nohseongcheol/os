#!/usr/bin/env python3
"""होस्ट libc 없이 연결한 नेपाली C 프로그램을 वास्तविक_लगत ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import अवास्तविक_मेशिन

स्थिति = Path(__file__).resolve().parents[1]

def कार्यान्वयन_गर्नुहोस्_आदेश():
    मापन = {}
    सर्भर_मान = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    सर्भर_मान.bind(('127.0.0.1', 0))
    सर्भर_मान.settimeout(0.1)
    접속번호 = सर्भर_मान.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                लगत, ठेगाना = सर्भर_मान.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(लगत)
            सर्भर_मान.sendto(लगत, ठेगाना)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            मेशिन = अवास्तविक_मेशिन(स्थिति / ('build/kernel.' + 종류), 종류)
            try:
                for दोहर्_याउनु_मान in range(2):
                    मेशिन.आदेश('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    मेशिन.आदेश('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                चलाउनुहोस् = len(मेशिन.लग_रेकर्ड)
                मेशिन.직렬.sendall(b'run posixinput\n')
                मेशिन.기다림('POSIX INPUT READY', चलाउनुहोस्)
                मेशिन.직렬.sendall(b'abcdef')
                출력 = मेशिन.기다림('jkoros> ', चलाउनुहोस्)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                मेशिन.आदेश('javac Hello.java', ['Exit: 0'])
                मेशिन.आदेश('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                मेशिन.आदेश('run hello recovered', ['arg: recovered', 'Exit: 0'])
                मापन[종류] = मेशिन.लग_रेकर्ड.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX फाइल/공유 स्थिति/삭제 수명/ठेगाना सुरक्षित_गर्नुहोस्_मान/UDP/표준 입력/기존 Java', flush=True)
            finally:
                मेशिन.बन्दगर्नुहोस्()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); सर्भर_मान.close()
    मापन['host_datagrams'] = [लगत.decode() for लगत in 받은자료]
    (स्थिति / 'build/규약시험.json').write_text(json.dumps(मापन, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    कार्यान्वयन_गर्नुहोस्_आदेश()
