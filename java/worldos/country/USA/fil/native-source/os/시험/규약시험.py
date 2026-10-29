#!/usr/bin/env python3
"""host libc 없이 연결한 한국어 C 프로그램을 totoo_data ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import virtual_machine

posisyon = Path(__file__).resolve().parents[1]

def Mag_execute_utos():
    sukat = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    numero_ng_port = server_VALUE.getsockname()[1]
    RECEIVED_data = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                data, email = server_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_data.append(data)
            server_VALUE.sendto(data, email)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            machine = virtual_machine(posisyon / ('build/kernel.' + 종류), 종류)
            try:
                for sprint_VALUE in range(2):
                    machine.utos('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    machine.utos('run posixudp ' + str(numero_ng_port), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                run = len(machine.LOG_hanay)
                machine.직렬.sendall(b'run posixinput\n')
                machine.maghintay_katayuan('POSIX INPUT READY', run)
                machine.직렬.sendall(b'abcdef')
                출력 = machine.maghintay_katayuan('jkoros> ', run)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                machine.utos('javac Hello.java', ['Exit: 0'])
                machine.utos('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                machine.utos('run hello recovered', ['arg: recovered', 'Exit: 0'])
                sukat[종류] = machine.LOG_hanay.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX file/공유 posisyon/삭제 수명/email magprotekta_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                machine.isara()
        assert b'posix-udp' in RECEIVED_data and b'truncate' in RECEIVED_data and b'' in RECEIVED_data
    finally:
        끝냄.set(); 일꾼.join(timeout=2); server_VALUE.close()
    sukat['host_datagrams'] = [data.decode() for data in RECEIVED_data]
    (posisyon / 'build/규약시험.json').write_text(json.dumps(sukat, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Mag_execute_utos()
