#!/usr/bin/env python3
"""òstair libc 없이 연결한 한국어 C 프로그램을 dearbh_dàta ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import mas_fhìor_inneal

suidhich = Path(__file__).resolve().parents[1]

def gnìomhaich_àithne():
    tomhas = {}
    frithealaiche_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    frithealaiche_VALUE.bind(('127.0.0.1', 0))
    frithealaiche_VALUE.settimeout(0.1)
    접속번호 = frithealaiche_VALUE.getsockname()[1]
    RECEIVED_dàta = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                dàta, ADDRESS = frithealaiche_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_dàta.append(dàta)
            frithealaiche_VALUE.sendto(dàta, ADDRESS)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            inneal = mas_fhìor_inneal(suidhich / ('build/kernel.' + 종류), 종류)
            try:
                for ath_thriall_VALUE in range(2):
                    inneal.àithne('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    inneal.àithne('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ruith = len(inneal.LOG_ràgh)
                inneal.직렬.sendall(b'run posixinput\n')
                inneal.fuirich_cor('POSIX INPUT READY', ruith)
                inneal.직렬.sendall(b'abcdef')
                출력 = inneal.fuirich_cor('jkoros> ', ruith)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                inneal.àithne('javac Hello.java', ['Exit: 0'])
                inneal.àithne('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                inneal.àithne('run hello recovered', ['arg: recovered', 'Exit: 0'])
                tomhas[종류] = inneal.LOG_ràgh.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX faidhle/공유 suidhich/삭제 수명/ADDRESS dìon_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                inneal.dùin()
        assert b'posix-udp' in RECEIVED_dàta and b'truncate' in RECEIVED_dàta and b'' in RECEIVED_dàta
    finally:
        끝냄.set(); 일꾼.join(timeout=2); frithealaiche_VALUE.close()
    tomhas['host_datagrams'] = [dàta.decode() for dàta in RECEIVED_dàta]
    (suidhich / 'build/규약시험.json').write_text(json.dumps(tomhas, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    gnìomhaich_àithne()
