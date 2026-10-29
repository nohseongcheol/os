#!/usr/bin/env python3
"""taurima libc 없이 연결한 Reo_Māori C 프로그램을 tūturu_raraunga ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import mariko_mīhini

tūranga = Path(__file__).resolve().parents[1]

def kawe_tono():
    mēhua = {}
    tūmau_uara = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tūmau_uara.bind(('127.0.0.1', 0))
    tūmau_uara.settimeout(0.1)
    접속번호 = tūmau_uara.getsockname()[1]
    RECEIVED_raraunga = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                raraunga, ADDRESS = tūmau_uara.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_raraunga.append(raraunga)
            tūmau_uara.sendto(raraunga, ADDRESS)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            mīhini = mariko_mīhini(tūranga / ('build/kernel.' + 종류), 종류)
            try:
                for whitiauau_uara in range(2):
                    mīhini.tono('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    mīhini.tono('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                whakahaere = len(mīhini.LOG_RECORD)
                mīhini.직렬.sendall(b'run posixinput\n')
                mīhini.기다림('POSIX INPUT READY', whakahaere)
                mīhini.직렬.sendall(b'abcdef')
                출력 = mīhini.기다림('jkoros> ', whakahaere)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                mīhini.tono('javac Hello.java', ['Exit: 0'])
                mīhini.tono('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                mīhini.tono('run hello recovered', ['arg: recovered', 'Exit: 0'])
                mēhua[종류] = mīhini.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Kōnae/공유 tūranga/삭제 수명/ADDRESS pare_uara/UDP/표준 입력/기존 Java', flush=True)
            finally:
                mīhini.Kati()
        assert b'posix-udp' in RECEIVED_raraunga and b'truncate' in RECEIVED_raraunga and b'' in RECEIVED_raraunga
    finally:
        끝냄.set(); 일꾼.join(timeout=2); tūmau_uara.close()
    mēhua['host_datagrams'] = [raraunga.decode() for raraunga in RECEIVED_raraunga]
    (tūranga / 'build/규약시험.json').write_text(json.dumps(mēhua, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    kawe_tono()
