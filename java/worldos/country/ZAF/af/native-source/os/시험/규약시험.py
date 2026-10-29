#!/usr/bin/env python3
"""hou libc 없이 연결한 한국어 C 프로그램을 werklik_data ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import virtueel_masjien

Posisie = Path(__file__).resolve().parents[1]

def uitvoer_bevel():
    maatreël = {}
    bediener_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bediener_VALUE.bind(('127.0.0.1', 0))
    bediener_VALUE.settimeout(0.1)
    접속번호 = bediener_VALUE.getsockname()[1]
    RECEIVED_data = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                data, adres = bediener_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_data.append(data)
            bediener_VALUE.sendto(data, adres)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            masjien = virtueel_masjien(Posisie / ('build/kernel.' + 종류), 종류)
            try:
                for sprint_VALUE in range(2):
                    masjien.Opdrag('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    masjien.Opdrag('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Loop = len(masjien.LOG_ry)
                masjien.직렬.sendall(b'run posixinput\n')
                masjien.wag_stand('POSIX INPUT READY', Loop)
                masjien.직렬.sendall(b'abcdef')
                Afvoer = masjien.wag_stand('jkoros> ', Loop)
                assert 'POSIX INPUT PASS' in Afvoer and 'Exit: 0' in Afvoer, Afvoer
                masjien.Opdrag('javac Hello.java', ['Exit: 0'])
                masjien.Opdrag('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                masjien.Opdrag('run hello recovered', ['arg: recovered', 'Exit: 0'])
                maatreël[종류] = masjien.LOG_ry.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Lêer/공유 Posisie/삭제 수명/adres beskerm_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                masjien.Sluit()
        assert b'posix-udp' in RECEIVED_data and b'truncate' in RECEIVED_data and b'' in RECEIVED_data
    finally:
        끝냄.set(); 일꾼.join(timeout=2); bediener_VALUE.close()
    maatreël['host_datagrams'] = [data.decode() for data in RECEIVED_data]
    (Posisie / 'build/규약시험.json').write_text(json.dumps(maatreël, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    uitvoer_bevel()
