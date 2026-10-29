#!/usr/bin/env python3
"""viesot libc 없이 연결한 Latviešu C 프로그램을 faktisks_dati ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import VM

Novietojums = Path(__file__).resolve().parents[1]

def Izpildīt_komanda():
    mērs = {}
    serveris_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serveris_VALUE.bind(('127.0.0.1', 0))
    serveris_VALUE.settimeout(0.1)
    porta_numurs = serveris_VALUE.getsockname()[1]
    RECEIVED_dati = []
    끝냄 = threading.Event()
    def atbalss_atbilde():
        while not 끝냄.is_set():
            try:
                dati, adrese = serveris_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_dati.append(dati)
            serveris_VALUE.sendto(dati, adrese)
    nodarbinātais_VALUE = threading.Thread(target=atbalss_atbilde, daemon=True)
    nodarbinātais_VALUE.start()
    try:
        for 종류 in ('elf', 'iso'):
            mašīna = VM(Novietojums / ('build/kernel.' + 종류), 종류)
            try:
                for sprints_VALUE in range(2):
                    mašīna.Komanda('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    mašīna.Komanda('run posixudp ' + str(porta_numurs), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Palaist = len(mašīna.LOG_RECORD)
                mašīna.직렬.sendall(b'run posixinput\n')
                mašīna.nogaides_stāvoklis('POSIX INPUT READY', Palaist)
                mašīna.직렬.sendall(b'abcdef')
                Izvade = mašīna.nogaides_stāvoklis('jkoros> ', Palaist)
                assert 'POSIX INPUT PASS' in Izvade and 'Exit: 0' in Izvade, Izvade
                mašīna.Komanda('javac Hello.java', ['Exit: 0'])
                mašīna.Komanda('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                mašīna.Komanda('run hello recovered', ['arg: recovered', 'Exit: 0'])
                mērs[종류] = mašīna.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Fails/공유 Novietojums/삭제 수명/adrese aizsargāt_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                mašīna.Aizvērt()
        assert b'posix-udp' in RECEIVED_dati and b'truncate' in RECEIVED_dati and b'' in RECEIVED_dati
    finally:
        끝냄.set(); nodarbinātais_VALUE.join(timeout=2); serveris_VALUE.close()
    mērs['host_datagrams'] = [dati.decode() for dati in RECEIVED_dati]
    (Novietojums / 'build/규약시험.json').write_text(json.dumps(mērs, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Izpildīt_komanda()
