#!/usr/bin/env python3
"""lletya libc 없이 연결한 Cymraeg C 프로그램을 go_iawn_data ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import rhith_peiriant

safle = Path(__file__).resolve().parents[1]

def Gweithredu_gorchymyn():
    mesur = {}
    gweinydd_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    gweinydd_VALUE.bind(('127.0.0.1', 0))
    gweinydd_VALUE.settimeout(0.1)
    rhif_porth = gweinydd_VALUE.getsockname()[1]
    RECEIVED_data = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                data, ADDRESS = gweinydd_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_data.append(data)
            gweinydd_VALUE.sendto(data, ADDRESS)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            peiriant = rhith_peiriant(safle / ('build/kernel.' + 종류), 종류)
            try:
                for iteriad_VALUE in range(2):
                    peiriant.Gorchymyn('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    peiriant.Gorchymyn('run posixudp ' + str(rhif_porth), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Gweithredu_2 = len(peiriant.LOG_rhes)
                peiriant.직렬.sendall(b'run posixinput\n')
                peiriant.aros_cyflwr('POSIX INPUT READY', Gweithredu_2)
                peiriant.직렬.sendall(b'abcdef')
                Allbwn = peiriant.aros_cyflwr('jkoros> ', Gweithredu_2)
                assert 'POSIX INPUT PASS' in Allbwn and 'Exit: 0' in Allbwn, Allbwn
                peiriant.Gorchymyn('javac Hello.java', ['Exit: 0'])
                peiriant.Gorchymyn('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                peiriant.Gorchymyn('run hello recovered', ['arg: recovered', 'Exit: 0'])
                mesur[종류] = peiriant.LOG_rhes.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Ffeil/공유 safle/삭제 수명/ADDRESS diogelu_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                peiriant.Cau()
        assert b'posix-udp' in RECEIVED_data and b'truncate' in RECEIVED_data and b'' in RECEIVED_data
    finally:
        끝냄.set(); 일꾼.join(timeout=2); gweinydd_VALUE.close()
    mesur['host_datagrams'] = [data.decode() for data in RECEIVED_data]
    (safle / 'build/규약시험.json').write_text(json.dumps(mesur, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Gweithredu_gorchymyn()
