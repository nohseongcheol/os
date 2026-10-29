#!/usr/bin/env python3
"""host libc 없이 연결한 한국어 C 프로그램을 stvarni_podaci ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import VM

pozicija = Path(__file__).resolve().parents[1]

def Izvrši_komanda():
    KR = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    broj_porta = server_VALUE.getsockname()[1]
    RECEIVED_podaci = []
    끝냄 = threading.Event()
    def eho_odgovor():
        while not 끝냄.is_set():
            try:
                podaci, adresa = server_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_podaci.append(podaci)
            server_VALUE.sendto(podaci, adresa)
    일꾼 = threading.Thread(target=eho_odgovor, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            računar = VM(pozicija / ('build/kernel.' + 종류), 종류)
            try:
                for sprint_VALUE in range(2):
                    računar.komanda('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    računar.komanda('run posixudp ' + str(broj_porta), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                koristiti = len(računar.LOG_snimi)
                računar.직렬.sendall(b'run posixinput\n')
                računar.stanje_čekanja('POSIX INPUT READY', koristiti)
                računar.직렬.sendall(b'abcdef')
                출력 = računar.stanje_čekanja('jkoros> ', koristiti)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                računar.komanda('javac Hello.java', ['Exit: 0'])
                računar.komanda('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                računar.komanda('run hello recovered', ['arg: recovered', 'Exit: 0'])
                KR[종류] = računar.LOG_snimi.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Datoteka/공유 pozicija/삭제 수명/adresa zaštititi_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                računar.Zatvori()
        assert b'posix-udp' in RECEIVED_podaci and b'truncate' in RECEIVED_podaci and b'' in RECEIVED_podaci
    finally:
        끝냄.set(); 일꾼.join(timeout=2); server_VALUE.close()
    KR['host_datagrams'] = [podaci.decode() for podaci in RECEIVED_podaci]
    (pozicija / 'build/규약시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Izvrši_komanda()
