#!/usr/bin/env python3
"""host libc 없이 연결한 Malti C 프로그램을 attwali_data ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import virtwali_kompjuter

pożizzjoni = Path(__file__).resolve().parents[1]

def eżegwixxa_kmand():
    miżura = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    접속번호 = server_VALUE.getsockname()[1]
    RECEIVED_data = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                data, ADDRESS = server_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_data.append(data)
            server_VALUE.sendto(data, ADDRESS)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            kompjuter = virtwali_kompjuter(pożizzjoni / ('build/kernel.' + 종류), 종류)
            try:
                for iterazzjoni_VALUE in range(2):
                    kompjuter.kmand('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    kompjuter.kmand('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                serje = len(kompjuter.LOG_RECORD)
                kompjuter.직렬.sendall(b'run posixinput\n')
                kompjuter.기다림('POSIX INPUT READY', serje)
                kompjuter.직렬.sendall(b'abcdef')
                출력 = kompjuter.기다림('jkoros> ', serje)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                kompjuter.kmand('javac Hello.java', ['Exit: 0'])
                kompjuter.kmand('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                kompjuter.kmand('run hello recovered', ['arg: recovered', 'Exit: 0'])
                miżura[종류] = kompjuter.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX fajl/공유 pożizzjoni/삭제 수명/ADDRESS pproteġa_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                kompjuter.agħlaq()
        assert b'posix-udp' in RECEIVED_data and b'truncate' in RECEIVED_data and b'' in RECEIVED_data
    finally:
        끝냄.set(); 일꾼.join(timeout=2); server_VALUE.close()
    miżura['host_datagrams'] = [data.decode() for data in RECEIVED_data]
    (pożizzjoni / 'build/규약시험.json').write_text(json.dumps(miżura, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    eżegwixxa_kmand()
