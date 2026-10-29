#!/usr/bin/env python3
"""organizuoti libc 없이 연결한 Lietuvių C 프로그램을 faktinis_duomenys ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import VM

Pozicija = Path(__file__).resolve().parents[1]

def Vykdyti_komanda():
    REZULTATAS = {}
    serveris_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serveris_VALUE.bind(('127.0.0.1', 0))
    serveris_VALUE.settimeout(0.1)
    prievado_numeris = serveris_VALUE.getsockname()[1]
    RECEIVED_duomenys = []
    끝냄 = threading.Event()
    def aidas_atsakyti():
        while not 끝냄.is_set():
            try:
                duomenys, ADDRESS = serveris_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_duomenys.append(duomenys)
            serveris_VALUE.sendto(duomenys, ADDRESS)
    darbininkas_VALUE = threading.Thread(target=aidas_atsakyti, daemon=True)
    darbininkas_VALUE.start()
    try:
        for 종류 in ('elf', 'iso'):
            mašina = VM(Pozicija / ('build/kernel.' + 종류), 종류)
            try:
                for sprintas_VALUE in range(2):
                    mašina.Komanda('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    mašina.Komanda('run posixudp ' + str(prievado_numeris), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Paleisti = len(mašina.LOG_RECORD)
                mašina.직렬.sendall(b'run posixinput\n')
                mašina.laukimo_būsena('POSIX INPUT READY', Paleisti)
                mašina.직렬.sendall(b'abcdef')
                Išvestis = mašina.laukimo_būsena('jkoros> ', Paleisti)
                assert 'POSIX INPUT PASS' in Išvestis and 'Exit: 0' in Išvestis, Išvestis
                mašina.Komanda('javac Hello.java', ['Exit: 0'])
                mašina.Komanda('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                mašina.Komanda('run hello recovered', ['arg: recovered', 'Exit: 0'])
                REZULTATAS[종류] = mašina.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Failas/공유 Pozicija/삭제 수명/ADDRESS apsaugoti_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                mašina.Užverti()
        assert b'posix-udp' in RECEIVED_duomenys and b'truncate' in RECEIVED_duomenys and b'' in RECEIVED_duomenys
    finally:
        끝냄.set(); darbininkas_VALUE.join(timeout=2); serveris_VALUE.close()
    REZULTATAS['host_datagrams'] = [duomenys.decode() for duomenys in RECEIVED_duomenys]
    (Pozicija / 'build/규약시험.json').write_text(json.dumps(REZULTATAS, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Vykdyti_komanda()
