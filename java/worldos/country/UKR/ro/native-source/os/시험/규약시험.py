#!/usr/bin/env python3
"""gazdă libc 없이 연결한 Română C 프로그램을 real_date ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import VM

Poziție = Path(__file__).resolve().parents[1]

def executa_comandă():
    KR = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    număr_port = server_VALUE.getsockname()[1]
    RECEIVED_date = []
    끝냄 = threading.Event()
    def ecou_replică():
        while not 끝냄.is_set():
            try:
                date, adresa = server_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_date.append(date)
            server_VALUE.sendto(date, adresa)
    일꾼 = threading.Thread(target=ecou_replică, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            mașină = VM(Poziție / ('build/kernel.' + 종류), 종류)
            try:
                for sprint_VALUE in range(2):
                    mașină.Comandă('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    mașină.Comandă('run posixudp ' + str(număr_port), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Pornește = len(mașină.LOG_RECORD)
                mașină.직렬.sendall(b'run posixinput\n')
                mașină.stare_de_așteptare('POSIX INPUT READY', Pornește)
                mașină.직렬.sendall(b'abcdef')
                Rezultat = mașină.stare_de_așteptare('jkoros> ', Pornește)
                assert 'POSIX INPUT PASS' in Rezultat and 'Exit: 0' in Rezultat, Rezultat
                mașină.Comandă('javac Hello.java', ['Exit: 0'])
                mașină.Comandă('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                mașină.Comandă('run hello recovered', ['arg: recovered', 'Exit: 0'])
                KR[종류] = mașină.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Fișier/공유 Poziție/삭제 수명/adresa proteja_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                mașină.Închide()
        assert b'posix-udp' in RECEIVED_date and b'truncate' in RECEIVED_date and b'' in RECEIVED_date
    finally:
        끝냄.set(); 일꾼.join(timeout=2); server_VALUE.close()
    KR['host_datagrams'] = [date.decode() for date in RECEIVED_date]
    (Poziție / 'build/규약시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    executa_comandă()
