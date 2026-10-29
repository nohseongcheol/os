#!/usr/bin/env python3
"""pritës libc 없이 연결한 한국어 C 프로그램을 aktual_të_dhëna ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import virtual_makinë

Pozicioni = Path(__file__).resolve().parents[1]

def zbatoj_komandë():
    llogaritje = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    numri_i_portës = server_VALUE.getsockname()[1]
    RECEIVED_të_dhëna = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                të_dhëna, email = server_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_të_dhëna.append(të_dhëna)
            server_VALUE.sendto(të_dhëna, email)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            makinë = virtual_makinë(Pozicioni / ('build/kernel.' + 종류), 종류)
            try:
                for përsëritje_VALUE in range(2):
                    makinë.Komanda('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    makinë.Komanda('run posixudp ' + str(numri_i_portës), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Ekzekuto = len(makinë.LOG_RECORD)
                makinë.직렬.sendall(b'run posixinput\n')
                makinë.Prit_status('POSIX INPUT READY', Ekzekuto)
                makinë.직렬.sendall(b'abcdef')
                출력 = makinë.Prit_status('jkoros> ', Ekzekuto)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                makinë.Komanda('javac Hello.java', ['Exit: 0'])
                makinë.Komanda('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                makinë.Komanda('run hello recovered', ['arg: recovered', 'Exit: 0'])
                llogaritje[종류] = makinë.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Kartelë/공유 Pozicioni/삭제 수명/email mbroj_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                makinë.Mbyll()
        assert b'posix-udp' in RECEIVED_të_dhëna and b'truncate' in RECEIVED_të_dhëna and b'' in RECEIVED_të_dhëna
    finally:
        끝냄.set(); 일꾼.join(timeout=2); server_VALUE.close()
    llogaritje['host_datagrams'] = [të_dhëna.decode() for të_dhëna in RECEIVED_të_dhëna]
    (Pozicioni / 'build/규약시험.json').write_text(json.dumps(llogaritje, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    zbatoj_komandë()
