#!/usr/bin/env python3
"""Host libc 없이 연결한 한국어 C 프로그램을 aktuell_Daten ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import virtuell_Computer

positionéieren = Path(__file__).resolve().parents[1]

def ausféieren_Befeel():
    Mooss = {}
    Server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Server_VALUE.bind(('127.0.0.1', 0))
    Server_VALUE.settimeout(0.1)
    접속번호 = Server_VALUE.getsockname()[1]
    RECEIVED_Daten = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                Daten, Adress = Server_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_Daten.append(Daten)
            Server_VALUE.sendto(Daten, Adress)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            Computer = virtuell_Computer(positionéieren / ('build/kernel.' + 종류), 종류)
            try:
                for Iteratioun_VALUE in range(2):
                    Computer.Befeel('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    Computer.Befeel('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Laf = len(Computer.LOG_Rei)
                Computer.직렬.sendall(b'run posixinput\n')
                Computer.Waart_Status('POSIX INPUT READY', Laf)
                Computer.직렬.sendall(b'abcdef')
                출력 = Computer.Waart_Status('jkoros> ', Laf)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                Computer.Befeel('javac Hello.java', ['Exit: 0'])
                Computer.Befeel('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                Computer.Befeel('run hello recovered', ['arg: recovered', 'Exit: 0'])
                Mooss[종류] = Computer.LOG_Rei.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Fichier/공유 positionéieren/삭제 수명/Adress schützen_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                Computer.Clôture()
        assert b'posix-udp' in RECEIVED_Daten and b'truncate' in RECEIVED_Daten and b'' in RECEIVED_Daten
    finally:
        끝냄.set(); 일꾼.join(timeout=2); Server_VALUE.close()
    Mooss['host_datagrams'] = [Daten.decode() for Daten in RECEIVED_Daten]
    (positionéieren / 'build/규약시험.json').write_text(json.dumps(Mooss, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ausféieren_Befeel()
