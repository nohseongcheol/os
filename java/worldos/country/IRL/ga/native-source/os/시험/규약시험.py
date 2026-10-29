#!/usr/bin/env python3
"""óstach libc 없이 연결한 Gaeilge C 프로그램을 iarbhír_sonraí ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import fíorúil_meaisín

suíomh = Path(__file__).resolve().parents[1]

def Rith_ordú():
    tomhas = {}
    freastalaí_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    freastalaí_VALUE.bind(('127.0.0.1', 0))
    freastalaí_VALUE.settimeout(0.1)
    uimhir_phoirt = freastalaí_VALUE.getsockname()[1]
    RECEIVED_sonraí = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                sonraí, ADDRESS = freastalaí_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_sonraí.append(sonraí)
            freastalaí_VALUE.sendto(sonraí, ADDRESS)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            meaisín = fíorúil_meaisín(suíomh / ('build/kernel.' + 종류), 종류)
            try:
                for atriall_VALUE in range(2):
                    meaisín.Ordú('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    meaisín.Ordú('run posixudp ' + str(uimhir_phoirt), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Rith_2 = len(meaisín.LOG_ró)
                meaisín.직렬.sendall(b'run posixinput\n')
                meaisín.기다림('POSIX INPUT READY', Rith_2)
                meaisín.직렬.sendall(b'abcdef')
                Aschur = meaisín.기다림('jkoros> ', Rith_2)
                assert 'POSIX INPUT PASS' in Aschur and 'Exit: 0' in Aschur, Aschur
                meaisín.Ordú('javac Hello.java', ['Exit: 0'])
                meaisín.Ordú('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                meaisín.Ordú('run hello recovered', ['arg: recovered', 'Exit: 0'])
                tomhas[종류] = meaisín.LOG_ró.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Comhad/공유 suíomh/삭제 수명/ADDRESS cosain_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                meaisín.Dún()
        assert b'posix-udp' in RECEIVED_sonraí and b'truncate' in RECEIVED_sonraí and b'' in RECEIVED_sonraí
    finally:
        끝냄.set(); 일꾼.join(timeout=2); freastalaí_VALUE.close()
    tomhas['host_datagrams'] = [sonraí.decode() for sonraí in RECEIVED_sonraí]
    (suíomh / 'build/규약시험.json').write_text(json.dumps(tomhas, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Rith_ordú()
